__all__ = (
    'AzureServiceBusConnectorInstance',
)

import logging

from .service import AzureServiceBusConnectorInstance


LOGGING = True

def set_default_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("siren_common_utility.log"), 
            logging.StreamHandler()          
        ]
    )
    logging.getLogger("azure.servicebus").setLevel(logging.WARNING)
    logging.getLogger("azure.core").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("uamqp").setLevel(logging.WARNING) 

if LOGGING:
    set_default_logger()




# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 서버 시작 시 백그라운드 리스너 실행
#     task = asyncio.create_task(sb_manager.start_listening_loop("topic", "sub"))
#     yield
#     # 서버 종료 시 태스크 취소
#     task.cancel()
#     try:
#         await task
#     except asyncio.CancelledError:
#         print("Listener task cancelled safely.")

