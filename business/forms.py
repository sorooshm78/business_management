from django import forms

from business import models


class RecordModelForm(forms.ModelForm):
    class Meta:
        model = models.Record

        exclude = [
            'repository',
            'category',
        ]

        widgets = {
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
                    'class': 'form-control',
                    'id': 'record_type',
                    'onchange': 'fillCategory()',
                },
            ),
            'category_display': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'cat_dis',
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
                    'type': 'text',
                    'id': 'date',
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
