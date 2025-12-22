import azure.functions as func
import logging
import json 
import requests
import os

app = func.FunctionApp()

backend_base_url = os.getenv("BACKEND_BASE_URL")
backend_base_port = os.getenv("BACKEND_BASE_PORT")

@app.service_bus_topic_trigger(arg_name="azservicebus", 
                               subscription_name="all",
                               topic_name="emc-patient-alert",
                               connection="sirengoldenhour_SERVICEBUS") 
def emc_patient_alert_servicebus_trigger(azservicebus: func.ServiceBusMessage):


    # /api/v1/emc/broadcast/to-centers/{region}

    body = azservicebus.get_body().decode("utf-8")
    msg_id = getattr(azservicebus, "message_id", "")
    corr_id = getattr(azservicebus, "correlation_id", "")
    sess_id = getattr(azservicebus, "session_id", "")
    region = azservicebus.user_properties.get("Region", "")

    
    
    try:
        payload = json.loads(body)
        region = region.split("|")[1:-1]
    except json.JSONDecodeError:
        logging.exception(f"Invalid JSON. msg_id={msg_id} body={body}")
        raise
    except AttributeError:
        logging.exception(f"Invalid Region format. msg_id={msg_id} region={region}")
        raise

    headers = {
        "Content-Type": "application/json",
        "x-message-id": msg_id,
        "x-correlation-id": corr_id,
    }

    logging.info(f"Regions to send: {region}")
    logging.info(f"azservicebus.user_properties tyep: {type(azservicebus.user_properties)}")
    logging.info(f"azservicebus.body: {type(body)}")
    for r in region:
        url = f"https://{backend_base_url}:{backend_base_port}/api/v1/emc/broadcast/to-centers/{r}"
        req_payload = {
            "topic_body": body,
            "topic_message_id": msg_id,
            "topic_correlation_id": corr_id,
            "topic_session_id": sess_id,
            "topic_properties": azservicebus.user_properties
        }

        logging.info(f"Payload sent to region {r}: {json.dumps(req_payload)}")
        try: 
            response = requests.post(url, 
                                     headers=headers, 
                                     json=req_payload, 
                                     verify=False)
            logging.info(f"Sent message to region {r}: {response.status_code}")
            logging.info(f"Payload sent to region {r}: {json.dumps(req_payload)}")
        except requests.RequestException as e:
            logging.exception(f"HTTP request failed. msg_id={msg_id} url={url}")
            raise

        if response.status_code >= 400:
            logging.error(f"Failed to send message to region {r}. msg_id={msg_id} status_code={response.status_code} response={response.text}")
            raise Exception(f"Failed to send message to region {r}. Status code: {response.status_code}")

        if response.status_code == 200:
            logging.info(f"Delivered to backend successfully msg_id={msg_id} region={r}")

        
@app.service_bus_topic_trigger(arg_name="azservicebus", 
                               subscription_name="all", 
                               topic_name="emc-center-response",
                               connection="sirengoldenhour_SERVICEBUS") 
def emc_center_response_servicebus_trigger(azservicebus: func.ServiceBusMessage):

    #  /api/v1/emc/broadcast/to-field/{tenant_id}
    body = azservicebus.get_body().decode("utf-8")
    msg_id = getattr(azservicebus, "message_id", "")
    corr_id = getattr(azservicebus, "correlation_id", "")
    sess_id = getattr(azservicebus, "session_id", "")

    try:
        payload = json.loads(body)
        tenant_id = payload.get("tenant_id")
    except json.JSONDecodeError:
        logging.exception(f"Invalid JSON. msg_id={msg_id} body={body}")
        raise
    headers = {
        "Content-Type": "application/json",
        "x-message-id": msg_id,
        "x-correlation-id": corr_id,
    }

    logging.info(f"Regions to send: {tenant_id}")
    logging.info(f"azservicebus.user_properties tyep: {type(azservicebus.user_properties)}")
    logging.info(f"azservicebus.body: {type(body)}")

    url = f"https://{backend_base_url}:{backend_base_port}/api/v1/emc/broadcast/to-field/{tenant_id}"
    req_payload = {
            "topic_body": body,
            "topic_message_id": msg_id,
            "topic_correlation_id": corr_id,
            "topic_session_id": sess_id,
            "topic_properties": azservicebus.user_properties
        }
    try:
        response = requests.post(url, 
                                 headers=headers, 
                                 json=req_payload,
                                 verify=False)
        logging.info(f"Sent message to tenant {tenant_id}: {response.status_code}")
    except requests.RequestException as e:
        logging.exception(f"HTTP request failed. msg_id={msg_id} url={url}")
        raise

    if response.status_code >= 400:
        logging.error(f"Failed to send message to tenant {tenant_id}. msg_id={msg_id} status_code={response.status_code} \n response={response.text}")
        raise Exception(f"Failed to send message to tenant {tenant_id}. Status code: {response.status_code}")

    if response.status_code == 200:
        logging.info(f"Delivered to backend successfully msg_id={msg_id} tenant_id={tenant_id}")
