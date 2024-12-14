from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Account
from .models import TodoTask
from rest_framework_simplejwt.tokens import RefreshToken

class TodoTaskAPITestCase(APITestCase):
    def setUp(self):
        """
        This will run before each test. Set up the necessary data, including creating a user and a task.
        """
        # Create a user
        self.user_data = {
            'first_name': 'Mathew',
            'last_name': 'Alex',
            'username': 'Supermathew',
            'email': 'dolikemathewalex@gmail.com',
            'phone_number': '9372945391',
            'password': 'password123',
        }
        self.user = Account.objects.create_user(**self.user_data)
        self.user.is_active = True
        self.user.save()

        # This will create a task 
        self.todo_task_data = {
            'title': 'Buy groceries',
            'description': 'Milk, eggs, bread',
        }
        self.todo_task = TodoTask.objects.create(user=self.user, **self.todo_task_data)

        #This are the links for various cases of task-api
        self.register_url = reverse('register')  # registrations
        self.login_url = reverse('login')  # login
        self.todo_task_list_create_url = reverse('task-list-create')  # create the task,list all the task
        self.todo_task_detail_url = reverse('task-detail', kwargs={'pk': self.todo_task.id})  # url for retriving,updating,deleting one particular task
        self.delete_all_tasks_url = reverse('delete-all-tasks')  # for deleting all tasks

        # token for authentication
        self.token = self.get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def get_token_for_user(self, user):
        """
        Helper method to get JWT token for a user.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_todo_task(self):
        """
        This is a test for creating a todo task 
        """
        data = {
            'title': 'Maths Assignments',
            'description': 'Need to complete the maths assignments or else less marks',
        }

        response = self.client.post(self.todo_task_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Task created successfully')
        self.assertIn('task', response.data)

    def test_get_todo_tasks(self):
        """
        Test retrieving all tasks for the authenticated user
        """
        response = self.client.get(self.todo_task_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Tasks retrieved successfully')
        self.assertIn('tasks', response.data)
        self.assertGreater(len(response.data['tasks']), 0)

    def test_get_todo_task(self):
        """
        This is a test to retrive the task by the ID.
        """
        response = self.client.get(self.todo_task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Task retrieved successfully')
        self.assertIn('task', response.data)

    def test_update_todo_task(self):
        """
        This is a test to update a specific task for authenticated users
        """
        data = {
            'title': 'This is a updated title',
            'description': 'The description is updated',
        }

        response = self.client.put(self.todo_task_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Task updated successfully')
        self.assertIn('task', response.data)

    def test_delete_todo_task(self):
        """
        This is a test to delete a spectific task for authenticated users
        """
        response = self.client.delete(self.todo_task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Task deleted successfully')

    def test_delete_all_tasks(self):
        """
        This a test to delete the task for authenticated users
        """
        response = self.client.delete(self.delete_all_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'All tasks deleted successfully')

    def test_create_todo_task_unauthenticated(self):
        """
        This a test to create the task when their is no token provided by the user
        """
        self.client.credentials()
        data = {
            'title': 'Complete project',
            'description': 'Finish writing tests for the project',
        }

        response = self.client.post(self.todo_task_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_todo_task_unauthenticated(self):
        """
        This is a test to update the task when user does not provide me token 
        """
        self.client.credentials()
        data = {
            'title': 'Updated task',
            'description': 'Updated description for the task',
        }

        response = self.client.put(self.todo_task_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_todo_task_unauthenticated(self):
        """
        This is a test to delete a particular task when user does not provide me the token
        """
        self.client.credentials()
        response = self.client.delete(self.todo_task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_all_tasks_unauthenticated(self):
        """
        This is the test to delete all the task when their is no token provided
        """
        self.client.credentials()
        response = self.client.delete(self.delete_all_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
