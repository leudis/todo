from django.db import models
from .util import Util

class Task(models.Model):
# To define linked list
#previous = models.ForeignKey(Task)
#next = models.ForeignKey(Task)

    #* title: * mandatory, * up to 100 chars
    title = models.CharField(null = False, blank = False, max_length=100)

    #* description: * non-mandatory, any amount of chars
    description = models.TextField(null = True, blank = True)

    #* completed: * mandatory, * boolean
    completed = models.BooleanField(default=False)
  
    #* priority: * mandatory, * you may choose how you want to represent this
    priority = models.IntegerField(null = False, default = -1)

    #* timestamp of creation: * mandatory
    timestamp = models.DateTimeField(auto_now_add = True)

    def save(self, priority = None, *args, **kwargs):
        _util = Util(Task)
        
        if self.id == None:
            new_max_priority = _util.newMaxPriority()
            self.priority = new_max_priority
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
