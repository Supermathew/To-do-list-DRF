from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Account

class AccountAPITestCase(APITestCase):

    def setUp(self):

        self.user_data = {
            'first_name': 'Mathew',
            'last_name': 'Alex',
            'username': 'mathewalex',
            'email': 'demomathewalex@gmail.com',
            'phone_number': '9372945391',
            'password': 'password123',
        }
        self.user = Account.objects.create_user(**self.user_data)
        self.user.is_active = True
        self.user.save()

        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register_user(self):
        """
        This is a test to test the user registrations
        """
        data = {
            'first_name': 'Mathew',
            'last_name': 'Alex',
            'username': 'Supermathew',
            'email': 'dolikemathewalex@gmail.com',
            'phone_number': '9372945391',
            'password': 'password123',
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['message'], 'Registration successful!')

    def test_register_user_missing_field(self):
        """
        This is a test to test the user registration without the required fields.
        """
        data = {
            'first_name': 'Mathew',
            'last_name': 'Alex',
            'username': 'Supermathew',
            'email': 'dolikemathewalex@gmail.com',
            # Missing phone_number and password
        }
        
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        self.assertEqual(response.data['errors'], 'All fields are required')

    def test_register_user_email_taken(self):
        """
        This is a test to test the user registration when the email is already taken.
        """
        data = {
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'username': 'charlie_brown',
            'email': self.user_data['email'],  # This email id is already taken
            'phone_number': '1122334455',
            'password': 'password123',
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        self.assertEqual(response.data['errors'], 'Email is already registered')

    def test_login_user(self):
        """
        This is a test to test the user login functionality
        """
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['message'], 'User login successfully')

    def test_login_invalid_credentials(self):
        """
        This is a test to test in case of invalid credentials
        """
        data = {
            'email': self.user_data['email'],
            'password': 'incorrectpassword'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_login_missing_field(self):
        """
        This is a test to conduct login with missing fields like email or password
        """
        data = {
            'email': self.user_data['email'],
            # Missing password
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
