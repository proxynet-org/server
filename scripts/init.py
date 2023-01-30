from users.models import User
from content.models import Message
from rest_framework.test import APIClient
from django.urls import reverse
from faker import Faker
fake = Faker()


# create an admin user  if it doesn't exist
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_user(
        username='admin',
        password='admin',
        # location is at Paris
        location='48.856614,2.3522219',
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()

# Create 10 users with a password and a location


def create_user(username, password, location):
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            password=password,
            location=location,
        )


def create_users():
    # create 5 users in Paris and 5 users in London

    # Paris
    create_user('user1', 'user1', '48.856614,2.3522219')
    create_user('user2', 'user2', '48.856614,2.3522219')
    create_user('user3', 'user3', '48.856614,2.3522219')
    create_user('user4', 'user4', '48.856614,2.3522219')
    create_user('user5', 'user5', '48.856614,2.3522219')

    # London
    create_user('user6', 'user6', '51.507351,-0.127758')
    create_user('user7', 'user7', '51.507351,-0.127758')
    create_user('user8', 'user8', '51.507351,-0.127758')
    create_user('user9', 'user9', '51.507351,-0.127758')
    create_user('user10', 'user10', '51.507351,-0.127758')


create_users()


def post_message():
    # loop from user1 to user10
    for i in range(1, 11):
        # if user has messages, continue
        user = User.objects.get(username='user{}'.format(i))
        if Message.objects.filter(user=user).exists():
            continue
        # post a message
        url = reverse('message-list')
        # login the user
        client = APIClient()
        user = User.objects.get(username='user{}'.format(i))
        client.force_authenticate(user=user)
        for j in range(10):
            client.post(url, {'text': fake.text()})


post_message()
