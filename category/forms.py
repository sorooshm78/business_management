from django import forms
from django.forms import ModelForm

from category.models import Category


class CategoryModelForm(ModelForm):
    class Meta:
        model = Category
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
