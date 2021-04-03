from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Max, F
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .util import Util

from .models import Task
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'api/task-list/',
        'List':'api/task-list/<str:completed>/',
        'Detail View':'api/task-detail/<str:pk>/',
        'Create':'api/task-create/',
        'Update':'api/task-update/<str:pk>/',
        'Complete':'api/task-complete/<str:pk>/',
        'Reprioritize':'task-reprioritize/<str:pk>/<str:pkBefore>/',
        'Delete':'api/task-delete/<str:pk>/',
        }

    return Response(api_urls)

# {
#     "title": "task new",
#     "description": "task new description",
# } 
@api_view(['POST'])
def taskCreate(request):
    _data = request.data

    task_data = {}
    task_data['title'] = _data['title'] if 'title' in _data else ""
    task_data['description'] = _data['description'] if 'description' in _data else ""
    task_data['completed'] = False
    
    serializer = TaskSerializer(data = task_data)
    
    response = {'data': "input error"}

    if serializer.is_valid() and task_data['title'] != "":
        serializer.save()
        response = serializer.data

    return Response(response)

## 'complete' variable accept True/true or False/false
@api_view(['GET'])
def taskList(request, completed = ""):
    tasks = Task.objects.all().order_by('-priority')
    tasks = tasks.filter(priority__gt = -1)
    _completed = completed.lower()
    
    if (_completed == "true" or _completed == "false"):
        tasks = tasks.filter(completed = _completed.capitalize())

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

# {
#     "title": "task update",
#     "description": "description task update",
# }
@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['GET'])
def taskComplete(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data={'title': task.title, 'completed': True})

    if serializer.is_valid():
        serializer.update(task, serializer.validated_data)

    return Response(serializer.data)

@api_view(['GET'])
def taskReprioritize(request, pk, pkBefore=None):
    # idBefore is the id of the task that we want to locate after the task to prioritize.
    # In case of not having this id we will place the task at a highest priority.
    _new_priority = 0
    task_to_prioritize = Task.objects.get(id=pk)

    taskBefore = None

    # get the highest priority task
    util = Util(Task)
    max_priority = util.maxPriority()
    
    if pkBefore != None:
        task_before = Task.objects.get(id=pkBefore)

        tasks_over_task_before = Task.objects.filter(priority__gt = task_before.priority).order_by('priority').first()

        if (task_to_prioritize.id != tasks_over_task_before.id):

            if (pk != pkBefore and task_before != None and tasks_over_task_before != None):
                prrty_range_min = task_before.priority
                prrty_range_max = tasks_over_task_before.priority
                range_length = prrty_range_max - prrty_range_min
                if range_length <= 5:
                    new_prrty_in_range = (((prrty_range_max + 100) - prrty_range_min) // 2) + prrty_range_min
                    tasks = Task.objects.filter(priority__gt = prrty_range_min).exclude(id = task_to_prioritize.id).update(priority=F('priority') + 100)
                    task_to_prioritize.priority = new_prrty_in_range
                    task_to_prioritize.save()
                else:
                    new_prrty_in_range = (range_length // 2) + prrty_range_min
                    task_to_prioritize.priority = new_prrty_in_range
                    task_to_prioritize.save()

                #tasks = Task.objects.filter(priority__gt = max_priority).exclude(id = task_to_prioritize.id).update(priority=F('priority') + 100)
                #task_to_prioritize.update(priority = util.newMaxPriority())

            elif(task_before != None and tasks_over_task_before == None):
                if (max_priority != task_to_prioritize.priority):
                    #tasks = Task.objects.filter(priority__lte = max_priority).exclude(id = task_to_prioritize.id).update(priority=F('priority') + 100)
                    task_to_prioritize.priority = util.newMaxPriority()
                    task_to_prioritize.save()
        
    else:
        if (max_priority != task_to_prioritize.priority):
                #tasks = Task.objects.filter(priority__lte = max_priority).exclude(id = task_to_prioritize.id).update(priority=F('priority') + 100)
                task_to_prioritize.priority = util.newMaxPriority()
                task_to_prioritize.save()

    response = "the task was reprioritized successfully"
    return Response(response)

@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response('Item succsesfully delete!')