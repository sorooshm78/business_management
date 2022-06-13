# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from business.models import Category, Repository
from category import forms


@method_decorator(login_required, 'dispatch')
class CategoryListView(ListView):
    template_name = 'category/list_categories.html'
    context_object_name = 'categories'
    model = Category

    def get_queryset(self):
        query = super().get_queryset()

        repo_id = self.kwargs.get('repo_id')
        user_id = self.request.user.id
        query = query.filter(repository_id=repo_id, repository__user_id=user_id)

        return query

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['repo_id'] = self.kwargs.get('repo_id')
        return context


@method_decorator(login_required, 'dispatch')
class CreateCategory(CreateView):
    form_class = forms.CategoryModelForm
    template_name = 'category/add_category.html'

    def get_success_url(self):
        repo_id = self.kwargs.get('repo_id')
        return reverse('list_categories', kwargs={'repo_id': repo_id})

    def form_valid(self, form):
        repo_id = self.kwargs.get('repo_id')
        user_id = self.request.user.id

        repository = Repository.objects.filter(id=repo_id, user_id=user_id).first()
        form.instance.repository = repository

        return super().form_valid(form)


@login_required
def del_category(request: HttpRequest, category_id):
    user_id = request.user.id

    category = Category.objects.filter(
        id=category_id,
        repository__user_id=user_id
    ).first()
    repo_id = category.repository_id
    category.delete()

    return redirect(reverse('list_categories', kwargs={'repo_id': repo_id}))
