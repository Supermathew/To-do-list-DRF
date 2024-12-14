from rest_framework import serializers
from .models import TodoTask

class TodoTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoTask
        fields = [
            'id', 'title', 'description', 
            'stage', 'priority', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']