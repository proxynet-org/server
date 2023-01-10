
from django.test import TestCase
from users.models import User
from zone.models import Zone 
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


# Test unauthenticated user cannot create a Zone


class TestZoneCreateUnauthenticatedTest(TestCase):

    def test_zone_create_unauthenticated(self):
        url = reverse('zone-list')
        response = self.client.post(url, {'location': '40.4167754,-3.7037901999999576','max_slots':30,'occupied_slots':15})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

# Test authenticated user can create a Zone


class TestZoneCreateAuthenticatedTest(TestCase):

    def setUp(self):
        # create a user
        self.url = reverse('zone-list')
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            # coodonates of spain
            location='40.4167754,-3.7037901999999576',
        )
        # login the user
        self.client.login(username='testuser', password='12345')

    def test_zone_create_authenticated(self):
        response = self.client.post(self.url, {'location': '40.4167754,-3.7037901999999576','max_slots':30,'occupied_slots':15})
        self.assertEqual(response.status_code, 201)
