from django.test import TestCase
from users.models import User
from content.models import Message
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


# Test unauthenticated user cannot create a message


class TestMessageCreateUnauthenticatedTest(TestCase):

    def test_message_create_unauthenticated(self):
        url = reverse('message-list')
        response = self.client.post(url, {'text': 'Hello World'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

# Test authenticated user can create a message


class TestMessageCreateAuthenticatedTest(TestCase):

    def setUp(self):
        # create a user
        self.url = reverse('message-list')
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            # coodonates of spain
            location='40.4167754,-3.7037901999999576',
        )
        # login the user
        self.client.login(username='testuser', password='12345')

    def test_message_create_authenticated(self):
        response = self.client.post(self.url, {'text': 'Hello World'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['text'], 'Hello World')
        self.assertEqual(response.data['location'],
                         '40.4167754,-3.7037901999999576')
