from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from content.models import Message
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class TestMessagesFromDistance(APITestCase):
    """
    in setup :
    create 3 users
    testuser1 is from Paris, France
    testuser2 is 1km away from testuser1
    testuser3 is in New York, USA
    """

    def setUp(self):
        self.url = reverse('message-list')
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='12345',
            # coodonates of Paris, France
            coordinates={
                "latitude": "48.856614",
                "longitude": "2.352222"
            }
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='12345',
            # coodonates of 1km away from Paris, France
            coordinates={
                "latitude": "48.864716",
                "longitude": "2.349014"
            }
        )
        self.user3 = User.objects.create_user(
            username='testuser3',
            password='12345',
            # coodonates of New York, USA
            coordinates={
                "latitude": "40.730610",
                "longitude": "-73.935242"
            }
        )

        # Each user post "Hello World" message

        self.client.force_authenticate(user=self.user1)
        self.client.post(self.url, {'text': 'Hello World, its me testuser1'})
        self.client.logout()

        self.client.force_authenticate(user=self.user2)
        self.client.post(self.url, {'text': 'Hello World, its me testuser2'})
        self.client.logout()

        self.client.force_authenticate(user=self.user3)
        self.client.post(self.url, {'text': 'Hello World, its me testuser3'})
        self.client.logout()

    def test_messages_from_distance(self):
        """
        testuser1 can see his message and testuser2 message
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['text'],
                         'Hello World, its me testuser1')
        self.assertEqual(response.data[1]['text'],
                         'Hello World, its me testuser2')
        self.client.logout()
        """
        same goes for testuser2
        """
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['text'],
                         'Hello World, its me testuser1')
        self.assertEqual(response.data[1]['text'],
                         'Hello World, its me testuser2')
        self.client.logout()
        """
        testuser3 can only see his own message
        """
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'],
                         'Hello World, its me testuser3')
