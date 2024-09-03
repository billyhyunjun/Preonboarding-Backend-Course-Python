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
