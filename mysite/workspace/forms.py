from django import forms
from django.forms import ModelForm, DateInput

from .models import Task


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['date_time', 'operator', 'outlet']
        widgets = {
            'date_time': DateInput(attrs={'type': 'date'}),
            'operator': forms.Select(attrs={'class': 'form-control'}),
            'outlet': forms.Select(attrs={'class': 'form-control'}),

        }
