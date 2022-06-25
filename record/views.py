from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from record import forms
from record.models import Record
from repository.models import Repository


@login_required
def del_record(request: HttpRequest, record_id):
    record = Record.objects.filter(id=record_id, repository__user_id=request.user.id).first()

    repo_id = record.repository.id
    repository = Repository.objects.filter(id=repo_id).first()

    calculate_price_when_del_record(repository, record.record_type, record.payment_type, record.price)

    record.delete()
    return redirect(reverse('detail_repository', kwargs={'repo_id': repo_id}))


@method_decorator(login_required, name='dispatch')
class UpdateRecordView(View):

    @staticmethod
    def get_record_by_id(record_id):
        return Record.objects.filter(id=record_id).first()

    def get(self, request: HttpRequest, record_id):
        record = UpdateRecordView.get_record_by_id(record_id)
        repository = Repository.objects.filter(id=record.repository.id).first()
        form = forms.RecordModelForm(
            instance=record,
            user=request.user,
            repo_id=repository.id,
            record_type=record.record_type
        )

        calculate_price_when_del_record(repository, record.record_type, record.payment_type, record.price)

        return render(request, 'business/update_record.html', {
            'form': form,
        })

    def post(self, request: HttpRequest, record_id):
        record = UpdateRecordView.get_record_by_id(record_id)
        repository = Repository.objects.filter(id=record.repository.id).first()
        form = forms.RecordModelForm(
            request.POST,
            instance=record,
            user=request.user,
            repo_id=repository.id,
            record_type=record.record_type
        )
        if form.is_valid():
            calculate_price_when_add_record(repository, record.record_type, record.payment_type, record.price)
            form.save()
            return redirect(f'/repo/{repository.id}')

        return render(request, 'business/update_record.html', {
            'form': form,
        })


@method_decorator(login_required, name='dispatch')
class CreateRecordView(CreateView):
    form_class = forms.RecordModelForm
    template_name = 'business/add_record.html'

    def get_form_kwargs(self):
        kwargs = super(CreateRecordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['record_type'] = self.request.GET.get('type')
        kwargs['repo_id'] = self.kwargs.get('repo_id')
        return kwargs

    def get_success_url(self):
        repo_id = str(self.kwargs.get('repo_id'))
        return reverse('detail_repository', kwargs={'repo_id': repo_id})

    def form_valid(self, form):
        repo_id = self.kwargs.get('repo_id')
        record_type = self.request.GET.get('type')
        repository = Repository.objects.filter(id=repo_id).first()
        payment_type = form.instance.payment_type
        price = form.instance.price

        form.instance.repository = repository
        form.instance.record_type = record_type
        calculate_price_when_add_record(repository, record_type, payment_type, price)
        return super().form_valid(form)


def calculate_price_when_add_record(repository, record_type, payment_type, price):
    if record_type == 'input':
        repository.add_price(payment_type, price)
    elif record_type == 'output':
        repository.sub_price(payment_type, price)


def calculate_price_when_del_record(repository, record_type, payment_type, price):
    if record_type == 'input':
        repository.sub_price(payment_type, price)
    elif record_type == 'output':
        repository.add_price(payment_type, price)
