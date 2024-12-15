from rest_framework import serializers
from .models import TodoTask
from datetime import datetime
from django.utils import timezone

class TodoTaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = TodoTask
        fields = [
            'id', 'title', 'description', 
            'stage', 'priority', 
            'created_at', 'updated_at', 
            'due_date', 'is_overdue'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_overdue']

    def get_is_overdue(self, obj):
        return obj.is_overdue()

    def validate_due_date(self, value):
        now = timezone.now()
        if value <= now:
            raise serializers.ValidationError("Due datetime must be a future date.")
        return value