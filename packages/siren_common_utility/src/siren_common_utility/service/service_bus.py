__all__ = (
    'AzureServiceBusConnectorInstance',
)

from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from typing import Optional, AsyncGenerator
from azure.servicebus import ServiceBusReceivedMessage
from typing import Optional

import logging

try:
    from ..modules.az_service_bus import AzureServiceBusSenderController
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(
        str(Path(__file__).parent.parent)
    )
    from modules.az_service_bus import AzureServiceBusSenderController

class AzureServiceBusConnectorInstance:
    """Azure Service Bus에 연결하고 토픽과 Subscription 작업을 수행한다."""
    CONN_RETRY = 3
    CONN_LOGGING = False

    def __init__(
            self,
            ns_connection_string: str,
    ) -> None:
        """Service Bus에 대한 서비스 구현 클래스이다.

        Args:
            ns_connection_string (str): 네임스페이스 연결 문자열을 입력한다. (RootManageSharedAccessKey)

        Examples:
        ```python
            import asyncio
            from time import time

            namespace = 'example_servicebus_namespace'
            az_service_bus_instance = AzureServiceBusConnectorInstance(
                namespace
            )

            # Topic Publisher
            topic = 'example_topic'
            region = 'Seoul'

            _body = f'Test {topic} body to {region} - {time()}'
            asyncio.run(
                az_service_bus_instance.send_to_topic(
                    topic,
                    messages=[ServiceBusMessage(_body, 
                                                application_properties={
                                                    "Region": region,
                                                    # "Severity": "High", 
                                                    # "Dept": "Internal"
                                                })
                    ]
                )
            )

        ```

        """
        self.__ns_connection_string = ns_connection_string
        self._client = ServiceBusClient.from_connection_string(
            conn_str=self.__ns_connection_string, 
            retry_total=self.CONN_RETRY,
            logging_enable=self.CONN_LOGGING
        )

    async def send_to_topic(
            self, 
            topic_name: str,
            messages: list[ServiceBusMessage]
    ):
        """해당 토픽으로 메세지를 전송한다.

        ServiceBusMessage 객체는 `from azure.servicebus import ServiceBusMessage`로 Import할 수 있다.   
        
        Args:
            messages: (list[ServiceBusMessage]): 서비스 버스에 전송할 메세지를 담는다.

            >>> ServiceBusMessage(
                '예시 환자에 대한 메세지 전파',
                application_properties={
                    "Region": "Seoul", 
                    "Severity": "High", 
                    "Dept": "Internal"
                }
            )

            >>> ServiceBusMessage(
                '예시 환자에 대한 응답 데이터 답변',
                correlation_id='39mde-dj39d-0e9dz....'  # message_id는 자동으로 할당된다.
            )
            
        """
        logging.info(f"Service Bus Client Connected! Topic: {topic_name}")
        # Topic에 대해 Sender를 얻는다.
        sender = self._client.get_topic_sender(topic_name=topic_name)
        
        async with sender:
            sender_controller = AzureServiceBusSenderController(sender)
            await sender_controller.async_send_a_list_of_messages(messages)


    async def listening_subscribe_from_topic(
        self, 
        topic_name: str, 
        subscription_name: str, 
        session_id: Optional[str] = None,
        receiver_max_wait_time: Optional[float]=None,
        # receiver_max_message_count: Optional[int]=1,
        receiver_additional_kwargs: Optional[dict]=None
    ) -> AsyncGenerator[ServiceBusReceivedMessage, None]:
        """
        Azure Service Bus Topic 구독으로부터 메시지를 실시간으로 스트리밍한다.  
        
        수신된 메세지를 제너레이터로 하나씩 바깥으로 던져주는 구조이다.  
            주의: yield 이후에 코드를 배치하면 외부 처리가 끝난 후 실행.    
            외부에서 에러 없이 처리되었다고 가정하고 메시지를 완료 처리.  

        **주의**
        yield된 경우 자동으로 complte_message를 내부적으로 수행.

        Args:
            topic_name (str): 수신 토픽 이름.
            subscription_name (str): 수신 구독 이름.
            session_id (Optional[str]): 특정 세션 ID. None일 경우 사용 가능한 세션을 자동으로 할당.

        Examples:

            ```python
            async def start_listening_loop(self, topic_name, subscription_name):
                retry_delay = 1 
                max_delay = 60  

                while True:
                    try:
                        async for msg in self.listening_subscribe_from_topic(topic_name, subscription_name):
                            retry_delay = 1 
                            await self.process_message(msg)
                    
                    except Exception as e:
                        print(f"연결 끊김 또는 오류 발생: {e}")
                        sleep_time = min(max_delay, retry_delay + random.uniform(0, 1))
                        print(f"{sleep_time:.1f}초 후 재연결")
                        await asyncio.sleep(sleep_time)
                        retry_delay *= 2
            ```

        Yields:
            ServiceBusReceivedMessage: 메세지 객체.

        """
        default_max_wait_time_if_no_session_id = 5

        reciever_kwargs = receiver_additional_kwargs or {}
        reciever_kwargs['max_wait_time'] = receiver_max_wait_time
        if not session_id and not reciever_kwargs['max_wait_time']:
            # 세션 ID 없이 호출할 때는 할당할 빈 세션을 찾는 시간 = max_wait_time
            reciever_kwargs['max_wait_time'] = default_max_wait_time_if_no_session_id

        try:
            if session_id:
                receiver = self._client.get_subscription_receiver(
                    topic_name=topic_name, 
                    subscription_name=subscription_name,
                    session_id=session_id,
                    **reciever_kwargs
                )
            else:
                receiver = self._client.get_subscription_receiver(
                    topic_name=topic_name, 
                    subscription_name=subscription_name,
                    **reciever_kwargs
                )

            async with receiver:
                print(f"Subscribe [{subscription_name}] 스트리밍 시작...")
                async for msg in receiver:
                    # 외부(Caller)로 메시지를 전달
                    yield msg
                    # 주의: yield 이후에 코드를 배치하면 외부 처리가 끝난 후 실행
                    # 외부에서 에러 없이 처리되었다고 가정하고 메시지를 완료 처리
                    await receiver.complete_message(msg)

        except Exception as e:
            print(f"Service Bus 수신 중 오류 발생: {e}")
            raise e

    #--------------------------------------------------
    #   :NOTE
    #   (주석처리) recieve_shortly_from_topic
    #   일정량의 메세지를 수신받으면 연결이 종료되는 함수
    #--------------------------------------------------
    # async def recieve_shortly_from_topic(
    #         self, 
    #         topic_name: str,
    #         *,
    #         subscription_name: str,
    #         session_id: Optional[str]=None,
    #         receiver_max_wait_time: Optional[float]=None,
    #         receiver_max_message_count: Optional[int]=1,
    #         receiver_additional_kwargs: Optional[dict]=None
    # ):
    #     # create a Service Bus client using the connection string
    #     receiver_kwargs = receiver_additional_kwargs or {}
    #     async with ServiceBusClient.from_connection_string(
    #         conn_str=self.__ns_connection_string,
    #         logging_enable=True
    #     ) as servicebus_client:
    #         async with servicebus_client:
    #             # get the Subscription Receiver object for the subscription
    #             receiver = servicebus_client.get_subscription_receiver(
    #                 topic_name=topic_name, 
    #                 subscription_name=subscription_name,
    #                 session_id=session_id,
    #                 # max_wait_time=5,
    #                 **receiver_kwargs
    #             )
    #             async with receiver:
    #                 received_msgs = await receiver.receive_messages(
    #                     max_wait_time=receiver_max_wait_time, 
    #                     max_message_count=receiver_max_message_count
    #                 )
    #                 for msg in received_msgs:
    #                     print("Received: " + str(msg))
    #                     # complete the message so that the message is removed from the subscription
    #                     await receiver.complete_message(msg)
    #                 if not received_msgs:
    #                     print(f"No messages from topic: {topic_name}, sub: {subscription_name}")
    #
