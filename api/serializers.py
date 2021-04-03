from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields ='__all__'

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.title)
        if validated_data.get('completed', instance.completed) == True:
            instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance