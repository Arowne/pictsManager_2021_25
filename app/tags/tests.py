import base64
from django.core.files import File

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from user.models import User
from .models import Tag


class TagTests(APITestCase):

    def setUp(self):
        self.access_token = None
        self.tags_id = None

        user = User.objects.create_superuser(
            last_name="Lastname",
            first_name="Firstname",
            email="exemple@exemple.com",
            username="exemple@exemple.com",
            password='password1234',
            is_superuser=True
        )

        regular_user = User.objects.create_user(
            last_name="Lastname",
            first_name="Firstname",
            email="regular@exemple.com",
            username="regular@exemple.com",
            password='password1234',
        )

    def test_create_tags_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tags_unlogin_user(self):

        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tags_missing_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        data = {
            "title": ""
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')
        data = response.json()

        self.assertTrue(True, data['errors']['title'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_tags_invalid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        data = {
            'title': 'skdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdj',
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')
        data = response.json()

        self.assertTrue(True, data['errors']['title'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tags_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create tags
        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')

        # Read all tags and get create tags id
        url = '/tags/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.tags_id = data[0]["public_id"]

        # Update tags
        data = {
            "title": "New Title"
        }

        url = '/tags/' + self.tags_id
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_tags_missing_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create tags
        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')

        # Read all tags and get create tags id
        url = '/tags/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.tags_id = data[0]["public_id"]

        # Update tags
        data = {
            "title": "",
        }

        url = '/tags/' + self.tags_id
        response = self.client.put(url, data, format='json')
        data = response.json()

        self.assertTrue(True, data['errors']['title'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tags_invalid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create tags
        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')

        # Read all tags and get create tags id
        url = '/tags/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.tags_id = data[0]["public_id"]

        data = {
            'title': 'skdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdj',
        }

        url = '/tags/' + self.tags_id
        response = self.client.put(url, data, format='json')
        data = response.json()

        self.assertTrue(True, data['errors']['title'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tags_unauthorize_user(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create tags
        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')

        # Read all tags and get create tags id
        url = '/tags/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.tags_id = data[0]["public_id"]

        url = '/token'
        data = {'username': 'regular@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Update tags
        data = {
            "title": "Title"
        }

        url = '/tags/' + self.tags_id
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_tags_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create tags
        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')

        # Read all tags and get create tags id
        url = '/tags/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.tags_id = data[0]["public_id"]

        url = '/tags/' + self.tags_id
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_all_tags_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')

        # Read all tags and get create tags id
        url = '/tags/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tags_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create tags
        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')

        # Read all tags and get create tags id
        url = '/tags/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.tags_id = data[0]["public_id"]

        url = '/tags/' + self.tags_id
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tags_unauthorize_user(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create tags
        data = {
            "title": "Title"
        }

        url = '/tags'
        response = self.client.post(url, data, format='multipart')

        # Read all tags and get create tags id
        url = '/tags/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.tags_id = data[0]["public_id"]

        url = '/token'
        data = {'username': 'regular@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        url = '/tags/' + self.tags_id
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
