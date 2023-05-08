from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View

from .forms import RegisterForm, UserEditForm, UserEditEmailForm, UserChangePasswordForm
from .models import Profile
from app_store.models import Order


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            fio = form.cleaned_data.get('fio')
            phone_number = form.cleaned_data.get('phone_number')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            Profile.objects.create(
                user=user,
                fio=fio,
                phone_number=phone_number
            )
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/user/account')
    else:
        form = RegisterForm()
    return render(request, 'app_users/register.html', context={'form': form})


class Account(View):
    def get(self, request):
        order = Order.objects.filter(user=request.user).last()
        return render(request, 'app_users/account.html', {'order': order})


class UserLoginView(LoginView):
    template_name = 'app_users/login.html'
    redirect_authenticated_user = True
    next_page = '/user/account'


class UserLogoutView(LogoutView):
    template_name = 'app_users/logout.html'
    next_page = '/user/login'


class UserEditView(View):
    def get(self, request):
        form = UserEditForm(instance=Profile.objects.get(user=request.user))
        email_form = UserEditEmailForm(instance=request.user)
        change_password_form = UserChangePasswordForm(request.user)
        return render(request, 'app_users/profile_.html', context={'form': form,
                                                                   'change_password_form': change_password_form,
                                                                   'email_form': email_form})

    def post(self, request):
        form = UserEditForm(data=request.POST, files=request.FILES, instance=Profile.objects.get(user=request.user))
        email_form = UserEditEmailForm(data=request.POST, instance=request.user)
        change_password_form = UserChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid() and email_form.is_valid():
            form.save()
            email_form.save()
        else:
            print(form.errors)
            print(email_form.errors)
        if change_password_form.is_valid():
            password1 = change_password_form.cleaned_data.get('new_password1')
            password2 = change_password_form.cleaned_data.get('new_password2')
            if password1 and password2:
                if password1 != password2:
                    change_password_form.add_error('__all__', 'Введенные пароли не совпадают!')
                else:
                    change_password_form.save()
                    user = authenticate(username=request.user.username,
                                        password=change_password_form.cleaned_data.get('new_password1'))
                    login(request, user)
        else:
            change_password_form.add_error('__all__', 'Введенные пароли не совпадают!')
            print(change_password_form.errors)
            return render(request, 'app_users/profile_.html', context={'form': form,
                                                                       'change_password_form': change_password_form,
                                                                       'email_form': email_form})
        return HttpResponseRedirect(f'/user/account')

