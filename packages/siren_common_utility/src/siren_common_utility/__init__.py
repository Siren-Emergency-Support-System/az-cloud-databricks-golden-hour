"""
# Siren Common Utility  
**Azure Service 및 기타 유틸리티 기능을 제공합니다.**  

Contact: github.com/histigma  

```python
# 예제 코드

import os
from siren_common_utility import AzureServiceBusConnectorInstance

NS_CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_NS_CONNECTION_STR")        # Azure Cloud의 보안 연결 문자열
AZ_SERVICEBUS_INSTANCE = AzureServiceBusConnectorInstance(NS_CONNECTION_STR)

async def test():
    wait AZ_SERVICEBUS_INSTANCE.send_to_topic(
        ...
    )

```

"""
from .core import *