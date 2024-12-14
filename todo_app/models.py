from django.db import models
from django.conf import settings

class TodoTask(models.Model):

    STAGE_CHOICES = [
        ('created', 'Created'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    
    title = models.CharField(max_length=200, help_text="Title of the task")
    description = models.TextField(help_text="Detailed description of the task")
    
    stage = models.CharField(
        max_length=20, 
        choices=STAGE_CHOICES, 
        default='created',
        help_text="Current stage of the task"
    )
    
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        help_text="Priority level of the task"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_stage_display()}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Todo Task'
        verbose_name_plural = 'Todo Tasks'