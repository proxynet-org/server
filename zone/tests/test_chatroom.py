from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from zone.models import Zone 
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json


class TestChatroom(APITestCase):

    def setUp(self):
        self.url = reverse('chatroom-list')
        # user a & user b live in Paris same coordinates
        self.user_a = User.objects.create_user(
            username='testuser',
            password='12345',
            coordinates={
                "latitude": "48.856614",
                "longitude": "2.3522219"
            }
        )
        self.user_b = User.objects.create_user(
            username='testuser2',
            password='12345',
            coordinates={
                "latitude": "48.856614",
                "longitude": "2.3522219"
            }
        )
        self.client_a = APIClient()
        self.client_a.force_authenticate(user = self.user_a)
        self.client_b = APIClient()
        self.client_b.force_authenticate(user = self.user_b)


    def test_create_chatroom(self):
        data = {
            "name" : "test chatroom",
            "description" : "test chatroom description",
            "capacity" : 10,
            "lifetime" : 10,
        }

        response = self.client_a.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], data['name'])
        self.assertEqual(response.json()['description'], data['description'])
        self.assertEqual(response.json()['capacity'], data['capacity'])
        self.assertEqual(response.json()['lifetime'], data['lifetime'])

        # check that user a and b can see the chatroom

        response = self.client_a.get(self.url)
        self.assertEqual(len(response.json()),1) # one created
            
        response = self.client_b.get(self.url)
        self.assertEqual(len(response.json()),1) # one created

        # user a joins the chatroom
        response = self.client_a.post(reverse('chatroom-join',kwargs={'pk': response.json()[0]['id']}))
        self.assertEqual(response.status_code, 200)

        # user a lists chatrooms
        response = self.client_a.get(self.url)
        self.assertEqual(len(response.json()),1) # one created
        self.assertEqual(response.json()[0]['joined'],True)

        # user b lists chatrooms
        response = self.client_b.get(self.url)
        self.assertEqual(len(response.json()),1) # one created
        self.assertEqual(response.json()[0]['joined'],False)

        # user b joins the chatroom
        response = self.client_b.post(reverse('chatroom-join',kwargs={'pk': response.json()[0]['id']}))
        self.assertEqual(response.status_code, 200)

        # user b lists chatrooms
        response = self.client_b.get(self.url)
        self.assertEqual(len(response.json()),1) # one created
        self.assertEqual(response.json()[0]['joined'],True)
        self.assertEqual(response.json()[0]['num_people'],2)
        chatroom_id = response.json()[0]['id']

        # user a sends a message
        data = {
            "text" : "test message from user a"
        }
        response = self.client_a.post(reverse('chatroom-messages',kwargs={'pk': chatroom_id}), data, format='json')
        self.assertEqual(response.status_code, 201)

        # user b lists messages
        response = self.client_b.get(reverse('chatroom-messages',kwargs={'pk': chatroom_id}))
        self.assertEqual(len(response.json()),1) # one created
        self.assertEqual(response.json()[0]['text'],data['text'])

        # user a creates a new chatroom
        data = {
            "name" : "test chatroom 2",
            "description" : "test chatroom description 2",
            "capacity" : 10,
            "lifetime" : 10,
        }

        response = self.client_a.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], data['name'])
        self.assertEqual(response.json()['description'], data['description'])

        # user a joins the new chatroom without leaving the previous one
        response = self.client_a.post(reverse('chatroom-join',kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
