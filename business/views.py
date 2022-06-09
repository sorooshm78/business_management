from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView

# Create your views here.
from business import models, forms


@login_required
def get_category_list(request: HttpRequest):
    record_type = request.GET.get('type')
    repo_id = request.GET.get('repo_id')

    categories = models.Category.objects.filter(repository_id=repo_id, record_type=record_type,
                                                repository__user_id=request.user.id)

    cat_list = []
    for cat in categories:
        cat_list.append((cat.name, cat.id))

    return JsonResponse({
        'list': cat_list
    })


@method_decorator(login_required, name='dispatch')
class CreateRecordView(CreateView):
    form_class = forms.RecordModelForm
    template_name = 'business/add_record.html'

    def get_success_url(self):
        repo_id = str(self.kwargs.get('repo_id'))
        return reverse('detail_repository', kwargs={'repo_id': repo_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repo_id'] = self.kwargs.get('repo_id')
        return context

    def form_valid(self, form):
        repo_id = self.kwargs.get('repo_id')
        category_id = form.instance.category_display

        form.instance.category = models.Category.objects.get(id=category_id)
        form.instance.repository = models.Repository.objects.get(id=repo_id)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class DetailRepositoryView(ListView):
    model = models.Record
    template_name = 'business/detail_repository.html'
    context_object_name = 'records'

    @staticmethod
    def get_sum_records(records):
        sum_records_val = 0
        for record in records:
            sum_records_val += record.price
        return sum_records_val

    def get_queryset(self):
        query = super().get_queryset()

        repo_id = self.kwargs.get('repo_id')
        user_id = self.request.user.id
        query = query.filter(repository__user_id=user_id, repository_id=repo_id).all()

        return query

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['sum_records'] = DetailRepositoryView.get_sum_records(self.get_queryset())
        context['repo'] = models.Repository.objects.filter(user_id=self.request.user.id,
                                                           id=self.kwargs.get('repo_id')).first()

        return context


@method_decorator(login_required, name='dispatch')
class RepositoryView(ListView):
    model = models.Repository
    template_name = 'business/list_repository.html'
    context_object_name = 'repositories'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user_id=self.request.user.id)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sum_cart'] = models.Repository.get_sum_cart(self.request.user.id)
        context['sum_cash'] = models.Repository.get_sum_cash(self.request.user.id)

        return context


@login_required
def del_repository(request: HttpRequest, repo_id):
    models.Repository.objects.filter(user_id=request.user.id, id=repo_id).delete()
    return redirect(reverse('list_repository'))


@login_required
def del_record(request: HttpRequest, record_id):
    record = models.Record.objects.filter(id=record_id, repository__user_id=request.user.id).first()
    repo_id = record.repository.id
    record.delete()
    return redirect(reverse('detail_repository', kwargs={'repo_id': repo_id}))


@method_decorator(login_required, name='dispatch')
class NewRepositoryView(View):
    def get(self, request: HttpRequest):
        return render(request, 'business/new_repository.html')

    def post(self, request: HttpRequest):
        repo_name = request.POST.get('repo_name')
        new_repo = models.Repository(
            user_id=request.user.id,
            name=repo_name,
        )
        new_repo.save()
        return redirect(reverse('list_repository'))
