from django.contrib import admin
from .models import Task
from django.contrib.auth.models import Group

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority')
    exclude = ('priority',)
    ordering = ('-priority',)

admin.site.register(Task, TaskAdmin)
# unregister the Group model from admin.
admin.site.unregister(Group)


