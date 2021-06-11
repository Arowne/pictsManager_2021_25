import base64
from django.core.files import File

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from user.models import User
from .models import Image


class ImageTests(APITestCase):

    def setUp(self):
        self.access_token = None
        self.images_id = None

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

    def test_create_images_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_images_unlogin_user(self):

        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_images_missing_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        data = {
            "image": "",
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')
        data = response.json()

        self.assertTrue(True, data['errors']['image'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_images_invalid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        data = {
            'image': 'skdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdj',
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')
        data = response.json()

        self.assertTrue(True, data['errors']['image'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_images_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')

        # Read all images and get create images id
        url = '/images/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.images_id = data[0]["public_id"]

        # Update images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images/' + self.images_id
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_images_missing_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')

        # Read all images and get create images id
        url = '/images/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.images_id = data[0]["public_id"]

        # Update images        
        data = {
            "image": "",
        }

        url = '/images/' + self.images_id
        response = self.client.put(url, data, format='json')
        data = response.json()

        self.assertTrue(True, data['errors']['image'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_images_invalid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')

        # Read all images and get create images id
        url = '/images/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.images_id = data[0]["public_id"]

        data = {
            'image': 'skdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdjskdjskjdksjksjskjdsksjdj',
        }

        url = '/images/' + self.images_id
        response = self.client.put(url, data, format='json')
        data = response.json()

        self.assertTrue(True, data['errors']['image'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_images_unauthorize_user(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')

        # Read all images and get create images id
        url = '/images/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.images_id = data[0]["public_id"]

        url = '/token'
        data = {'username': 'regular@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Update images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images/' + self.images_id
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_images_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')

        # Read all images and get create images id
        url = '/images/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.images_id = data[0]["public_id"]

        self.client.credentials(HTTP_AUTHORIZATION='')

        url = '/images/' + self.images_id
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_all_images_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')

        # Read all images and get create images id
        url = '/images/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_images_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')

        # Read all images and get create images id
        url = '/images/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.images_id = data[0]["public_id"]

        url = '/images/' + self.images_id
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_images_unauthorize_user(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        # Create images
        image_file = open('./images/data/data.png', 'rb')
        data = {
            "image": image_file,
        }

        url = '/images'
        response = self.client.post(url, data, format='multipart')

        # Read all images and get create images id
        url = '/images/all'
        response = self.client.get(url, format='json')
        data = response.json()
        self.images_id = data[0]["public_id"]

        url = '/token'
        data = {'username': 'regular@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])

        url = '/images/' + self.images_id
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)