from django import forms

from business import models


class RecordModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        repo_id = kwargs.pop('repo_id')
        record_type = kwargs.pop('record_type')
        super(RecordModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = models.Category.objects.filter(
            repository_id=repo_id,
            record_type=record_type,
            repository__user_id=user.id,
        )

    class Meta:
        model = models.Record

        exclude = [
            'repository',
            'record_type',
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
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
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
