from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('task-list/', views.TaskCreateListView.as_view(), name="task-list"),
    path('task-list/<str:completed>/', views.TaskCreateListView.as_view(), name="task-list"),
    path('task/<str:pk>/', views.TaskDetailUpdateDeleteView.as_view(), name="task"),
    path('task-complete/<str:pk>/', views.TaskComplete.as_view(), name="task-complete"),
    path('task-reprioritize/<str:pk>/', views.TaskReprioritize.as_view(), name="task-reprioritize"),
    path('task-reprioritize/<str:pk>/<str:pkBefore>/', views.TaskReprioritize.as_view(), name="task-reprioritize"),
]