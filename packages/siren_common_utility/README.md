# Siren Common Utility

## 빠른 시작

사용하려는 Azure Function, 패키지/모듈 등에서 아래와 같이 사용하세요.

```sh
pip install <release-link>
```

클라우드 환경에서 사용할 경우, `requirements.txt`에 `pip install <release-link>` 와 같이 작성해야 합니다.

**예시:**

```ini
azure-functions
https://github.com/AnticSignal/stock-hyper-visioning-app/releases/download/v0.1.0_antic_ext/antic_extensions-0.1.0-py3-none-any.whl
certifi==2025.7.9
```

## 개발 테스트

```sh
pip install -e .
```

```sh
# Pytest
pytest --log-cli-level=DEBUG -s
```
