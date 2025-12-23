import azure.functions as func
import logging
import json 
import requests
import aiohttp
import asyncio
import os

app = func.FunctionApp()

backend_base_url = os.getenv("BACKEND_BASE_URL")
backend_base_port = os.getenv("BACKEND_BASE_PORT")

# 동시성 제한 (외부 백엔드 보호)
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "10"))
_semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

# 타임아웃
TIMEOUT_SEC = int(os.getenv("HTTP_TIMEOUT_SEC", "10"))
_client_timeout = aiohttp.ClientTimeout(total=TIMEOUT_SEC)

target_regions = ["Chungcheong","Gangwon","Gyeonggi","Honam","Incheon","Seoul","Yeongnam"]  #허용된 지역 목록

def _parse_regions(raw_region: str):
    # 기존 로직 유지: "xxx|a|b|c|" 같은 형태 가정
    # region.split("|")[1:-1]
    parts = raw_region.split("|")
    return parts[1:-1]

async def _post_to_region(
    session: aiohttp.ClientSession,
    url: str,
    headers: dict,
    req_payload: dict,
    msg_id: str,
    region: str,
) -> dict:
    async with _semaphore:
        try:
            async with session.post(url, headers=headers, json=req_payload, ssl=False) as resp:
                text = await resp.text()
                ok = 200 <= resp.status < 300
                return {
                    "region": region,
                    "status": resp.status,
                    "ok": ok,
                    "response_text": text[:2000],
                }
        except Exception as e:
            logging.exception(f"Exception during POST to region: {region}. msg_id={msg_id} url={url}")
            return {
                "region": region,
                "status": None,
                "ok": False,
                "error": str(e),
            }


@app.service_bus_topic_trigger(
        arg_name="azservicebus", 
        subscription_name="all",
        topic_name="emc-patient-alert",
        connection="sirengoldenhour_SERVICEBUS") 
async def emc_patient_alert_servicebus_trigger(azservicebus: func.ServiceBusMessage):


    # /api/v1/emc/broadcast/to-centers/{region}
    body = azservicebus.get_body().decode("utf-8")

    msg_id = getattr(azservicebus, "message_id", "") or ""
    corr_id = getattr(azservicebus, "correlation_id", "") or ""
    sess_id = getattr(azservicebus, "session_id", "") or ""

    user_properties = azservicebus.user_properties or {}
    region = user_properties.get("Region", "")

    
    
    try:
        payload = json.loads(body)
        regions = _parse_regions(region)
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

    logging.info(f"Regions to send: {regions}")
    logging.info(f"azservicebus.user_properties tyep: {type(user_properties)}")
    logging.info(f"azservicebus.body: {type(body)}")

    async with aiohttp.ClientSession(timeout=_client_timeout) as session:
        tasks = []
        for r in regions:
            if not r in target_regions:
                logging.warning(f"Skipping invalid region: {r}. msg_id={msg_id}")
                continue
            
            url = f"https://{backend_base_url}:{backend_base_port}/api/v1/emc/broadcast/to-centers/{r}"
            req_payload = {
                "topic_body": body,
                "topic_message_id": msg_id,
                "topic_correlation_id": corr_id,
                "topic_session_id": sess_id,
                "topic_properties": user_properties
            }
            logging.info(f"Prepared payload for region {r}: {json.dumps(req_payload)}")
            tasks.append(
                _post_to_region(
                    session,
                    url,
                    headers,
                    req_payload,
                    msg_id,
                    r,
                )
            )

        results = await asyncio.gather(*tasks, return_exceptions=False)
    
    failures = [r for r in results if not r.get("ok")]
    for r in results:
        if r.get("ok"):
            logging.info(f"Delivered to backend successfully msg_id={msg_id} region={r['region']}")
        else:
            logging.error(
                f"Failed to send message msg_id={msg_id} region={r.get('region')} "
                f"status={r.get('status')} error={r.get('error')} response={r.get('response_text')}"
            )
    if failures:
        raise Exception(f"One or more regions failed. msg_id={msg_id} failures={len(failures)}/{len(results)}")


        
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
