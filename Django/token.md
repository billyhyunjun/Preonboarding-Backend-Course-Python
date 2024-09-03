# Access / Refresh Token 발행과 검증에 관한 테스트 시나리오 작성하기
Django 프레임워크를 이용한 JWT Access / Refresh Token 발행과 검증 시나리오 작성입니다.

## Django 프로젝트 설치
* Django 설치
```bash
pip install django
```

* Django 프로젝트 생성
```bash
django-admin startproject testdjango
```

* Django 앱 생성
```bash
python manage.py startapp accounts
```

* 라이브러리 설치
```bash
pip install django djangorestframework djangorestframework-simplejwt
```

* settings.py
![image](https://github.com/user-attachments/assets/ce9956da-421d-413b-9f97-c456aa8a9e56)

![image](https://github.com/user-attachments/assets/41522f33-7d46-47bc-b306-2509fdd81693)


* JWT 발행과 검증을 위한 API 구현
[views.py](accounts/views.py)
```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class TokenObtainPairView(APIView):
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(APIView):
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
* URL 설정
[urls.py](testdjango/urls.py)
```python
from django.urls import path
from accounts.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

* 서버 오픈

![image](https://github.com/user-attachments/assets/74550bc9-c9d0-4948-9f4a-cc68b1729baf)


* 토큰 발급 테스트
  postman을 이용한 로그인 토큰 발급 테스트
![image](https://github.com/user-attachments/assets/b29bd7c3-5de7-433f-ade6-712bf2357bf9)


* 리프레쉬 토큰을 이용한 토큰 재발급

![image](https://github.com/user-attachments/assets/a38d9d36-73c4-4b87-96bc-9f8f61703370)

