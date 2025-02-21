from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ("not_completed", "Not Completed"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_completed")

    def __str__(self):
        return self.title
