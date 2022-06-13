from django import forms
from django.forms import ModelForm

from business import models


class CategoryModelForm(ModelForm):
    class Meta:
        model = models.Category
        exclude = [
            'repository'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'record_type': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }
