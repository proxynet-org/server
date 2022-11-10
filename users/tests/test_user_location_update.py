from users.models import User
from content.models import Message
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from rest_framework import status


class TestUpdateUserLocation(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username='user_a',
            password='user_a',
            # Paris location
            location='48.856614,2.3522219',
        )

        self.user_b = User.objects.create_user(
            username='user_b',
            password='user_b',
            # London location
            location='51.507351,-0.127758',
        )

        self.user_a_client = APIClient()
        self.user_a_client.login(username='user_a', password='user_a')

        self.user_b_client = APIClient()
        self.user_b_client.login(username='user_b', password='user_b')

    def test_update_user_location(self):
        # user_a posts "Hi from Paris" message

        url = reverse('message-list')
        data = {
            'text': 'Hi from Paris',
        }
        response = self.user_a_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # user_b sees no messages

        response = self.user_b_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # user_b moves to paris

        url = reverse('user-update-location')
        data = {
            'location': '48.856614,2.3522219',
        }
        response = self.user_b_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user_b sees the message

        url = reverse('message-list')
        response = self.user_b_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], 'Hi from Paris')
