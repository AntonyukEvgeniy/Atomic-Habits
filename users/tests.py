from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()
class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('users:register')
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'city': 'Test City',
            'phone': '+1234567890'
        }
    def test_valid_registration(self):
        """Тест успешной регистрации пользователя"""
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.city, 'Test City')

    def test_invalid_passwords(self):
        """Тест регистрации с несовпадающими паролями"""
        payload = self.valid_payload.copy()
        payload['password2'] = 'wrongpass123'

        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_duplicate_username(self):
        """Тест регистрации с существующим именем пользователя"""
        User.objects.create_user(
            username='testuser',
            email='existing@example.com',
            password='existingpass123'
        )
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
class TokenTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token_url = reverse('users:token_obtain_pair')
        self.refresh_url = reverse('users:token_refresh')
        self.valid_credentials = {
            'username': 'testuser',
            'password': 'testpass123'
        }
    def test_obtain_token(self):
        """Тест получения токена"""
        response = self.client.post(self.token_url, self.valid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    def test_invalid_credentials(self):
        """Тест получения токена с неверными учетными данными"""
        invalid_credentials = {
            'username': 'testuser',
            'password': 'wrongpass123'
        }
        response = self.client.post(self.token_url, invalid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_refresh_token(self):
        """Тест обновления токена"""
        # Сначала получаем токены
        response = self.client.post(self.token_url, self.valid_credentials, format='json')
        refresh_token = response.data['refresh']
        # Используем refresh токен для получения нового access токена
        response = self.client.post(
            self.refresh_url,
            {'refresh': refresh_token},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    def test_invalid_refresh_token(self):
        """Тест обновления токена с неверным refresh токеном"""
        response = self.client.post(
            self.refresh_url,
            {'refresh': 'invalid_token'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)