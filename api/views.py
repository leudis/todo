from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max, F
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .util import Util

from .models import Task

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
    'Overview': 'api',
    'List and Create': 'api/task/list',
    'List filter': 'api/task/list/true or false',
    'Detail, Update,Delete': 'task/<str:pk>/',
    'Complete': 'task-complete/<str:pk>/',
    'Reprioritize': 'task-reprioritize/<str:pk>/ (put the task to highest priority)',
    'Reprioritize before': 'task-reprioritize/<str:pk>/<str:pkBefore>/ (put the task with pk before task with pkBefore)'
    }

    return Response(api_urls)

class TaskCreateListView(ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        tasks = Task.objects.all().order_by('-priority')
        tasks = tasks.filter(priority__gt=-1)
        _completed = self.kwargs.get("completed", "").lower()

        if (_completed == "true" or _completed == "false"):
            tasks = tasks.filter(completed=_completed=="true")
        return tasks

class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class TaskComplete(APIView):
    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(instance=task, data={'title': task.title, 'completed': True})

        if serializer.is_valid():
            serializer.update(task, serializer.validated_data)

        return Response(serializer.data)


class TaskReprioritize(APIView):
    def post(self, request, pk, pkBefore=None):
        # idBefore is the id of the task that we want to locate after the task to prioritize.
        # In case of not having this id we will place the task at a highest priority.
        _new_priority = 0
        task_to_prioritize = Task.objects.get(id=pk)

        taskBefore = None

        # get the highest priority task
        _util = Util(Task)
        max_priority = _util.maxPriority()

        if pkBefore != None:
            
            if int(pkBefore) == -1:
                tasks = Task.objects.all().update(priority=F('priority') + 100)
                task_to_prioritize.priority = 0
                task_to_prioritize.save()
                return Response("the task was reprioritized to the lowest priority")

            task_before = Task.objects.get(id=pkBefore)

            tasks_over_task_before = Task.objects.filter(priority__gt=task_before.priority).order_by('priority').first()

            if (task_to_prioritize.id != tasks_over_task_before.id):

                if (pk != pkBefore and task_before != None and tasks_over_task_before != None):
                    prrty_range_min = task_before.priority
                    prrty_range_max = tasks_over_task_before.priority
                    range_length = prrty_range_max - prrty_range_min
                    if range_length <= 5:
                        new_prrty_in_range = (((prrty_range_max + 100) - prrty_range_min) // 2) + prrty_range_min
                        tasks = Task.objects.filter(priority__gt=prrty_range_min).exclude(id=task_to_prioritize.id).update(
                            priority=F('priority') + 100)
                        task_to_prioritize.priority = new_prrty_in_range
                        task_to_prioritize.save()
                    else:
                        new_prrty_in_range = (range_length // 2) + prrty_range_min
                        task_to_prioritize.priority = new_prrty_in_range
                        task_to_prioritize.save()

                elif (task_before != None and tasks_over_task_before == None):
                    if (max_priority != task_to_prioritize.priority):
                        task_to_prioritize.priority = _util.newMaxPriority()
                        task_to_prioritize.save()

        else:
            if (max_priority != task_to_prioritize.priority):
                task_to_prioritize.priority = _util.newMaxPriority()
                task_to_prioritize.save()

        response = "the task was reprioritized successfully"
        return Response(response)