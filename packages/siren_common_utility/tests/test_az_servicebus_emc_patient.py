import pytest
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

from azure.servicebus import ServiceBusMessage
from siren_common_utility import AzureServiceBusConnectorInstance
try:
    from siren_common_utility.src.siren_common_utility.service.service_bus import AzureServiceBusConnectorInstance
except:
    pass

from utils.service_bus import start_subscribe_listening_loop

load_dotenv()


NS_CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_NS_CONNECTION_STR")

# Environment variable checking
assert bool(NS_CONNECTION_STR)

# Init
AZ_SERVICEBUS_INSTANCE = AzureServiceBusConnectorInstance(NS_CONNECTION_STR)


async def test_az_servicebus_pub_to_emc_patient_alert():
    """emc_pateint_alert 토픽에 대해 Pub 테스트.
    """
    # Topic Publisher
    topic = 'emc-patient-alert'
    region = 'Gangwon'

    _body = f'Test body to {region} - {datetime.now()}'
    print(f"Sending to topic({topic}): {_body}")
    # asyncio.run(
    await AZ_SERVICEBUS_INSTANCE.send_to_topic(
        topic,
        messages=[
            ServiceBusMessage(_body, 
                            application_properties={
                                "Region": region,
                                # "Severity": "High", 
                                # "Dept": "Internal"
                            }
            )
        ]
    )
    # )
    print("Done sending messages")


@pytest.mark.asyncio
async def test_az_servicebus_receive_from_emc_patient_alert():
    """토픽 Subscriber
    """
    topic = 'emc-patient-alert'
    subscription_name = 'gangwon'

    try:
        async with asyncio.timeout(5): 
            await start_subscribe_listening_loop(
                AZ_SERVICEBUS_INSTANCE,
                topic, 
                subscription_name
            )
    except TimeoutError:
        print("3초 경과로 인한 자동 종료")
            
