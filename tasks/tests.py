from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task

class TaskOwnershipMiddlewareTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(title='Test Task', description='Task description', due_date='2024-02-14', status='Pending', owner=self.user)

    def test_owner_can_retrieve_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_retrieve_task(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        updated_data = {'title': 'Updated Task', 'description': 'Updated description', 'due_date': '2024-02-15', 'status': 'In Progress'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, updated_data['title'])

    def test_non_owner_cannot_update_task(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        updated_data = {'title': 'Updated Task', 'description': 'Updated description', 'due_date': '2024-02-15', 'status': 'In Progress'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.title, updated_data['title'])

    def test_owner_can_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)

    def test_non_owner_cannot_delete_task(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
