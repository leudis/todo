from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('task-list/', views.taskList, name="task-list"),
    path('task-list/<str:completed>/', views.taskList, name="task-list"),
    path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
    path('task-create/', views.taskCreate, name="task-create"),
    path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
    path('task-complete/<str:pk>/', views.taskComplete, name="task-complete"),
    path('task-reprioritize/<str:pk>/', views.taskReprioritize, name="task-reprioritize"),
    path('task-reprioritize/<str:pk>/<str:pkBefore>/', views.taskReprioritize, name="task-reprioritize"),
    path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
]