from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from content.models import Message
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class TestPublicationCreation(APITestCase):
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

    def test_publication_creation(self):
        data = {
            'title': 'Hi from Paris',
            'text': 'Hi from Paris',
        }
        response = self.user_a_client.post(reverse('publication-list'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['user'], self.user_a.id)
        self.assertEqual(response.data['coordinates'], self.user_a.coordinates)
        self.assert_(response.data['num_likes'] == 0)