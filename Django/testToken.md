# Pytest를 이용한 JWT Unit 테스트 코드 작성해보기
django에서 작성된 [views.py](../accounts/views.py)에서 [test.py](../accounts/tests.py)를 작성하여 테스트 코드 작성 

## TokenObtainPairViewTestCase

* test_valid_credentials: 유효한 사용자 이름과 비밀번호로 토큰을 요청하고, 응답에서 access와 refresh 토큰이 포함되어 있는지 확인합니다.
* test_invalid_credentials: 잘못된 사용자 이름과 비밀번호로 요청하고, 응답이 400 Bad Request인지 확인합니다.

## TokenRefreshViewTestCase

* setUp: 테스트를 위해 유저를 생성하고, 유효한 토큰을 발급받습니다.
* test_valid_refresh_token: 유효한 리프레시 토큰으로 액세스 토큰을 새로 발급받고, 응답에서 access 토큰이 포함되어 있는지 확인합니다.
* test_invalid_refresh_token: 유효하지 않은 리프레시 토큰으로 요청하고, 응답이 400 Bad Request인지 확인합니다.

```python
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class TokenObtainPairViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('token_obtain_pair')  # 'token_obtain_pair'는 URL 패턴 이름

    def test_valid_credentials(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_credentials(self):
        data = {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

class TokenRefreshViewTestCase(APITestCase):
    def setUp(self):
        self.refresh_url = reverse('token_refresh')  # 'token_refresh'는 URL 패턴 이름

        # Create a user and get access and refresh tokens
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.obtain_pair_url = reverse('token_obtain_pair')
        response = self.client.post(self.obtain_pair_url, {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json')
        self.refresh_token = response.data['refresh']

    def test_valid_refresh_token(self):
        data = {
            'refresh': self.refresh_token
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_invalid_refresh_token(self):
        # Use a clearly invalid token for testing
        data = {
            'refresh': 'thisisnotavalidjwt'
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Token is invalid or expired')

```

## 테스트 결과
![image](https://github.com/user-attachments/assets/6c913775-da55-46b6-83b5-1c4678a103ad)
