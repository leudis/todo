from django.db.models import Max

class Util:
    _task = None
    def __init__(self, task):
        self._task = task

    def newMaxPriority(self):
        max_priority_aggr = self._task.objects.aggregate(Max('priority'))['priority__max']
        max_priority_task =  self._task.objects.filter(priority = max_priority_aggr).first()
        new_max_priority = 0 if max_priority_task == None else max_priority_task.priority
        new_max_priority = new_max_priority + 100 if max_priority_task != None else new_max_priority
        return new_max_priority

    def maxPriority(self):
        max_priority_aggr = self._task.objects.aggregate(Max('priority'))['priority__max']
        max_priority_task =  self._task.objects.filter(priority = max_priority_aggr).first()
        max_priority = -1 if max_priority_task == None else max_priority_task.priority
        return max_priority