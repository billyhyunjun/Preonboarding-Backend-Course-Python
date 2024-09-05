# swagger UI
Swagger UI는 API를 문서화하고 테스트할 수 있는 웹 기반 사용자 인터페이스입니다. 주로 다음과 같은 기능을 제공합니다:

* 문서화 : API의 엔드포인트, 요청 및 응답 형식, 인증 방법 등 API의 구조와 사용법을 시각적으로 보여줍니다. 이를 통해 개발자는 API의 기능을 쉽게 이해할 수 있습니다.
* 테스트 : Swagger UI를 사용하면 API의 각 엔드포인트를 직접 호출해볼 수 있습니다. 이를 통해 실제 요청을 보내고 응답을 확인함으로써 API가 예상대로 작동하는지 쉽게 테스트할 수 있습니다.
* 자동화 : Swagger UI는 코드에서 자동으로 문서를 생성합니다. 즉, API를 정의하는 코드가 변경되면 Swagger UI도 자동으로 업데이트됩니다.
* 설명 및 예제 : Swagger UI는 API 엔드포인트에 대한 설명, 파라미터, 응답 형식 등을 명확하게 보여줍니다. 또한 예제 요청과 응답을 제공하여 API의 사용법을 직관적으로 이해할 수 있도록 도와줍니다.

## Django에 반영하기

### pip 설치
```bash
pip install drf-yasg
```

### settings.py 설정 추가
```python
# settings.py

INSTALLED_APPS = [
    # 기타 앱들
    'rest_framework',
    'drf_yasg',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
}
```

### url.py 추가
```python
from django.urls import path
from accounts.views import TokenObtainPairView, TokenRefreshView, RegisterView, LoginView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Testdjango",
        default_version='v1',
        description="Test description",
    ),
    public=True,
)

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
```

### 접속

* 메인

![image](https://github.com/user-attachments/assets/ac5ee532-385f-49c0-95f7-949bab8dd3f8)

* 로그인 인증 확인
![image](https://github.com/user-attachments/assets/ebc29563-00ac-4856-8f64-2e1dfd1a0273)
![image](https://github.com/user-attachments/assets/c9baf161-0e5a-4d6a-802b-fc9208fd3736)



