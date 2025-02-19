from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("inprogress", "In Progress"),
        ("not_completed", "Not Completed"),
    ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)

    class Meta:
        model = Task
        fields = ["title", "description", "status"]
