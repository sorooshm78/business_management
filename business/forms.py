from django import forms

from business import models


class RecordModelForm(forms.ModelForm):
    class Meta:
        model = models.Record
        fields = '__all__'
        widgets = {
            'repository': forms.TextInput(
                attrs={
                    'type': 'hidden',
                    'class': 'form-control'
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'payment_type': forms.Select(
                attrs={
                    'class': 'form-control'
                },
            ),
            'record_type': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'price': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                }
            ),
            'date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),

        }
