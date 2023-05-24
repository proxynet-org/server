
from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from zone.models import Zone 
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json


# Test unauthenticated user cannot create a Zone


class TestZoneCreateUnauthenticatedTest(APITestCase):

    def test_zone_create_unauthenticated(self):
        url = reverse('zone-list')
        response = self.client.post(url, {'coordinates': {'latitude': 40.4167754, 'longitude': -3.7037901999999576}, 'max_slots': 30, 'occupied_slots': 15}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

# Test authenticated user can create a Zone


class TestZoneCreateAuthenticatedTest(APITestCase):

    def setUp(self):
        # create a user
        self.url = reverse('zone-list')
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            # coodonates of spain
            coordinates={
                "latitude": "40.4167754",
                "longitude": "-3.7037901999999576"
            }
        )
        # login the user
        self.client.force_authenticate(user = self.user)

    def test_zone_crud_authenticated(self):
        # create / list view
        data = {'coordinates': {'latitude': 40.4167754, 'longitude': -3.7037901999999576}, 'max_slots': 30, 'occupied_slots': 15}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)

        # read / list view
        response = self.client.get(reverse('zone-list'))
        self.assertEqual(len(response.json()),1) # one created
        self.assertEqual(response.json()[0],data)

        # read / detail view
        id = Zone.objects.all().first().id
        response = self.client.get(reverse('zone-detail',kwargs={'pk': id}))
        self.assertEqual(response.json(),data)

        # update / detail view
        data['max_slots'] = 40
        response = self.client.put(reverse('zone-detail',kwargs={'pk': id}),json.dumps(data),
                                content_type="application/json")
        self.assertEqual(response.json(),data)
        self.assertEqual(response.json()['max_slots'],40)

        # delete / detail view
        response = self.client.delete(reverse('zone-detail',kwargs={'pk': id}))
        response = self.client.get(reverse('zone-list'))
        self.assertEqual(len(response.json()),0) # empty

