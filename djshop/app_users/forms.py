from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    fio = forms.CharField(max_length=90, required=True, help_text='ФИО')
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserEditForm(forms.ModelForm):

    fio = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'Profile-file form-input',
        'data-validate':  'onlyImgAvatar'
    }))

    class Meta:
        model = Profile
        fields = ['fio', 'phone_number', 'avatar']


class UserEditEmailForm(forms.ModelForm):

    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'E-mail'
    }))

    class Meta:
        model = User
        fields = ['email']


class UserChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        required=False,
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": 'form-input',
                                          "placeholder": "Тут можно изменить пароль"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        required=False,
        label="New password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": "form-input",
                                          "placeholder": "Введите пароль повторно"}),
        strip=False,
    )

