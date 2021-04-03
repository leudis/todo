from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Task
from django.urls import reverse
from rest_framework import status
import json

from rest_framework.test import APIRequestFactory

def tasks_create():
    # {
    #     "title": "new task",
    #     "description": "new task description"
    # }
    for t in range(10):
        Task.objects.create(title = "new task " + str(t), description = "new task description " + str(t))

class TaskViewTests(APITestCase):
    def test_task_prioritize(self):
        tasks_create()

        task_id = 1
        url_reprioritize = reverse('task-reprioritize', args=(task_id,))
        response_reprioritize = self.client.get(url_reprioritize)
        self.assertEqual(response_reprioritize.status_code, status.HTTP_200_OK)
        
        url_list = reverse('task-list')
        response_list = self.client.get(url_list)
        reprioritized_task_id = json.loads(response_list.content)[0]['id']
        print("reprioritized task id:" + str(reprioritized_task_id))
        print("tasks list:" + str(json.loads(response_list.content)))

        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(reprioritized_task_id, 1)

    def test_task_prioritize_2(self):
        tasks_create()

        task_to_reprioritize_id = 3
        task_followed_by_reprioritized_id = 9

        url_reprioritize = reverse('task-reprioritize', args=(task_to_reprioritize_id,task_followed_by_reprioritized_id))
        response_reprioritize = self.client.get(url_reprioritize)
        self.assertEqual(response_reprioritize.status_code, status.HTTP_200_OK)
        
        url_list = reverse('task-list')
        response_list = self.client.get(url_list)
        
        reprioritized_task_id = json.loads(response_list.content)[1]['id']
        
        print("reprioritized task id = 3:" + str(reprioritized_task_id))
        print("tasks list 2:" + str(json.loads(response_list.content)))

        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(reprioritized_task_id, 3)

        task_before_reprioritized_task_id = json.loads(response_list.content)[2]['id']
        self.assertEqual(task_before_reprioritized_task_id, 9)

    def test_task_list(self):
        tasks_create()
        
        url_list = reverse('task-list')
        response_list = self.client.get(url_list)
        
        list_content = json.loads(response_list.content)
        print("tasks list:" + str(list_content))

        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_content), 10)