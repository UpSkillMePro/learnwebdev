from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class CreateUserViewTest(APITestCase):
    """Test for the CreateUserView."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user:create')

    def test_create_user(self):
        """Test creating a new user."""
        payload = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)


class CreateTokenViewTest(APITestCase):
    """Test for the CreateTokenView."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.url = reverse('user:token')

    def test_create_token(self):
        """Test token creation for user."""
        payload = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class ManageUserViewTest(APITestCase):
    """Test for the ManageUserView."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user:update')

    def test_retrieve_user(self):
        """Test retrieving the profile for logged in user."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user(self):
        """Test updating the user profile for authenticated user."""
        payload = {'email': 'newemail@example.com',
                   'password': 'newpassword123'}

        response = self.client.patch(self.url, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
