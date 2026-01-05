# 골든 아워 - 실시간 응급 환자 지원 및 의료 빅데이터 분석 인사이트 플랫폼

**실시간 응급 환자 지원을 위한 Azure Cloud 및 Databricks 기반 실시간 분산 시스템과 MIT LCP 의료 빅데이터 분석 서비스**

[![GitHub Projects](https://img.shields.io/badge/GitHub%20Projects-222222?style=for-the-badge&logo=github&logoColor=white)](https://github.com/orgs/Siren-Emergency-Support-System/projects/1)  [![GitHub Discussions](https://img.shields.io/badge/GitHub%20Discussions-333333?style=for-the-badge&logo=github&logoColor=white)](https://github.com/orgs/Siren-Emergency-Support-System/discussions)  [![Confluence](https://img.shields.io/badge/Confluence-0052CC?style=for-the-badge&logo=confluence&logoColor=white)](https://histigma.atlassian.net/wiki/spaces/MDS/pages/294927)

## 프로젝트 개요

본 프로젝트는 클라우드 기반의 인프라 구현과 백엔드 구축으로 대규모 확장 가능한 IT 솔루션 아키텍처 제작을 위하여 구성되었습니다.

| 팀명/프로젝트명 | Siren - 골든아워 플랫폼                                             |
| :-------------- | :------------------------------------------------------------------ |
| 기간            | 준비 기간: 시작일 전 2~4일<br />2025. 12. 12 ~ 2025. 12. 23. (12일) |
| 인원            | 강민영 김혁수 신동환 이대건 조민기                                  |
| 주제            | 신속한 응급 환자 이송 및 지원 플랫폼                                |
| 기술            | 하단 `주요 기술` 항목 참조.                                       |

### 원천 데이터 및 API

[![MIT LCP](https://img.shields.io/badge/MIT%20LCP-A31F34?style=for-the-badge&logo=Massachusetts-Institute-of-Technology&logoColor=white)](https://lcp.mit.edu/)   [![MIMIC-IV-ED](https://img.shields.io/badge/MIMIC--IV-4B0082?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAARElEQVQ4y2NgGAWjYBSMglEACf7/B2E6A0SAmYGBgYWBgYGRmZmZAV0An6Y/YGBgYGZkZGRkZGBgYMCX9EAGjIJRMApGAAIAOksDAtA/5WAAAAAASUVORK5CYII=&logoColor=white)](https://physionet.org/content/mimiciv/)    [![Public Data](https://img.shields.io/badge/Public%20Data-003399?style=for-the-badge&logo=data.gov&logoColor=white)](https://www.data.go.kr/)    [![NCP](https://img.shields.io/badge/Naver%20Cloud%20Platform-03C75A?style=for-the-badge&logo=naver&logoColor=white)](https://www.ncloud.com/)

### 기술적 특징

* 의료 빅데이터에 대한 `Azure Databricks`를 활용한 거버넌스 확립 및 데이트 파이프라인 통합 구축
* 실시간 분산 시스템 기반으로 확장 가능한 클라우드 기반 AMQP 구조를 채택

### 주요 기술

| **항목**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 내용           |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| [![Azure](https://img.shields.io/badge/Microsoft-Azure-blue?logo=microsoft-azure&style=flat-square)](https://azure.microsoft.com/)   [![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat-square&logo=databricks&logoColor=white)](https://www.databricks.com/)   [![Azure Functions](https://img.shields.io/badge/Azure-Functions-purple?logo=azure-functions&style=flat-square)](https://azure.microsoft.com/services/functions/)   [![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-teal?logo=openai&style=flat-square)](https://learn.microsoft.com/azure/cognitive-services/openai/)   [![Azure Service Bus](https://img.shields.io/badge/Azure%20Service%20Bus-0078D4?style=flat-square&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/services/service-bus/) | Cloud Infra    |
| [![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)  ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)   ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)  [![Oracle DB](https://img.shields.io/badge/Oracle%20DB-F80000?style=flat-square&logo=oracle&logoColor=white)](https://www.oracle.com/database/)    [![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)                                                                                                                                                                                          | BE / FE        |
| [![Confluence](https://img.shields.io/badge/Confluence-172B4D?style=flat-square&logo=confluence&logoColor=white)](https://www.atlassian.com/software/confluence)   [![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)](https://git-scm.com/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | DevOps / Tools |
