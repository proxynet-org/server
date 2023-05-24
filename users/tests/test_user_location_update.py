from users.models import User
from content.models import Message
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status


class TestUpdateUserLocation(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username='user_a',
            password='user_a',
            # Paris location
            coordinates={
                "latitude": "48.856614",
                "longitude": "2.352222"
            }
        )

        self.user_b = User.objects.create_user(
            username='user_b',
            password='user_b',
            # London location
            coordinates={
                "latitude": "51.507351",
                "longitude": "-0.127758"
            }
        )

        self.user_a_client = APIClient()
        self.user_a_client.force_authenticate(user=self.user_a)

        self.user_b_client = APIClient()
        self.user_b_client.force_authenticate(user=self.user_b)

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

        url = reverse('update-user-location')
        data = {
            'coordinates': {
                "latitude": "48.856614",
                "longitude": "2.3522219"
            }
        }
        response = self.user_b_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user_b sees the message

        url = reverse('message-list')
        response = self.user_b_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], 'Hi from Paris')
