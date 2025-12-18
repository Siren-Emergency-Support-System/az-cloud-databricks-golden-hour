from azure.servicebus import ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusAuthenticationError
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from azure.servicebus.aio import ServiceBusSender

__all__ = (
    'AzureServiceBusSenderController',
)

class AzureServiceBusSenderController:

    def __init__(
            self,
            sender: "ServiceBusSender"
    ) -> None:
        """Azure Service Bus에 대해 전송자 메서드를 지원한다.

        Args:
            sender (_type_): Sender 객체를 넘겨준다.

        Examples:

            ```python
            async def run():
                # create a Service Bus client using the connection string
                async with ServiceBusClient.from_connection_string(
                    conn_str=NAMESPACE_CONNECTION_STR,
                    logging_enable=True) as servicebus_client:
                    # Get a Topic Sender object to send messages to the topic
                    sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
                    async with sender:
                        # Sender
                        controller = AzureServiceBusSenderController(sender)
                        ...
                        
            ```
        """
        self._sender = sender

    async def async_send_single_message(self, message: ServiceBusMessage):
        try:
            # send the message to the topic
            await self._sender.send_messages(message)
        except ServiceBusAuthenticationError:
            logging.error(
                "ServiceBusAuthentication Error: "
                "Set credentials or topic name correctly!"
            )
            raise

    async def async_send_a_list_of_messages(
            self,
            messages: list[ServiceBusMessage]
    ):
        try:
            # send the list of messages to the topic
            await self._sender.send_messages(messages)
            print(f"Sent a list of {len(messages)} messages")
        except ServiceBusAuthenticationError:
            logging.error(
                "ServiceBusAuthentication Error: "
                "Set credentials or topic name correctly!"
            )
            raise

    async def async_send_batch_message(
            self,
            messages: list[ServiceBusMessage]
    ):
        try:
            # Create a batch of messages
            async with self._sender:
                batch_message = await self._sender.create_message_batch()
                for msg in messages:
                    try:
                        # Add a message to the batch
                        batch_message.add_message(msg)
                    except ValueError:
                        # ServiceBusMessageBatch object reaches max_size.
                        # New ServiceBusMessageBatch object can be created here to send more data.
                        break
                # Send the batch of messages to the topic
                await self._sender.send_messages(batch_message)
        except ServiceBusAuthenticationError:
            logging.error(
                "ServiceBusAuthentication Error: "
                "Set credentials or topic name correctly!"
            )
            raise

