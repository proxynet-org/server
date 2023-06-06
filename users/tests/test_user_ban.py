from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from content.models import Message
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class TestBannedUser(APITestCase):

    def setUp(self):
        # create a user
        self.url = reverse('message-list')
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            # coodonates of spain
            coordinates='40.4167754,-3.7037901999999576',
        )
        self.user.ban_duration = 100
        self.user.ban_date = timezone.now()
        self.user.save()

    def test_message_create_authenticated(self):
        # user login and send message with jwt token
        user_refresh = RefreshToken.for_user(self.user)
        jwt_tokens = {
            'refresh': str(user_refresh),
            'access': str(user_refresh.access_token),
        }

        # send message using this jwt token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_tokens['access'])

        message_data = {
            'text': 'Hello, this is a test message.',
        }

        response = self.client.post(self.url, message_data)
        self.assertEqual(response.status_code, 401)

    def test_obtain_token(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password' : '12345',
        }
        client = APIClient()
        response = client.post(url, data)
        self.assertEqual(response.status_code, 403)

