from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_completed', 'Not Completed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_completed')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)  
    
    def __str__(self):
        return self.title
