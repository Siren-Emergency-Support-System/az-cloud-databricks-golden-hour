import asyncio
import random

async def start_subscribe_listening_loop(
        servicebus_instance,
        topic_name, 
        subscription_name
):
    """Subscribe에 대해 Listening Loop 흐름을 생성할 수 있습니다."""
    retry_delay = 1 
    max_delay = 60 

    while True:
        try:
            async for msg in servicebus_instance.listening_subscribe_from_topic(
                    topic_name, 
                    subscription_name
                ):
                retry_delay = 1 
                print('메세지 받음:', msg)
        
        except Exception as e:
            print(f"연결 끊김 또는 오류 발생: {e}")
            sleep_time = min(max_delay, retry_delay + random.uniform(0, 1))
            print(f"{sleep_time:.1f}초 후 재연결을 시도합니다...")
            await asyncio.sleep(sleep_time)
            retry_delay *= 2

