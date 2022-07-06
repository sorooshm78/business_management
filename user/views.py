from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from user import forms


@method_decorator(login_required, name='dispatch')
class ChangePassView(FormView):
    form_class = forms.ChangePassModelForms
    template_name = 'user/change_password.html'

    def get_success_url(self):
        logout(self.request)
        return reverse('login')

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        new_password = form.cleaned_data.get('new_password')
        user = User.objects.get(id=self.request.user.id)

        if user.check_password(password):
            user.set_password(new_password)
            user.save()
        else:
            form.add_error('password', 'رمز فعلی صحیح نمی باشد')
            return super().form_invalid(form)

        return super().form_valid(form)


class LoginView(FormView):
    form_class = forms.LoginModelForms
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse('list_repository')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = User.objects.filter(username=username, is_superuser=False).first()
        if user is None:
            form.add_error('username', 'شما اجازه ورود ندارید')
            return super().form_invalid(form)

        if not user.check_password(password):
            form.add_error('username', 'رمز اشتباه')
            return super().form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('login'))
