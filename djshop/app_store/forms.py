from django import forms
from .models import Feedback
from app_users.models import Profile


class ReviewAddForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-textarea',
                                                                       'placeholder': 'Review'}))

    class Meta:
        model = Feedback
        fields = ('text',)


class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(required=False, initial=1, widget=forms.HiddenInput)


class OrderProfileForm(forms.ModelForm):
    fio = forms.CharField(required=True, widget=forms.TextInput())
    phone_number = forms.CharField()

    class Meta:
        model = Profile
        fields = ['fio', 'phone_number']


ORDER_DELIVERY_TYPE_SELECT = [('Обычная доставка KEY', 'Обычная доставка VALUE'),
                              ('Экспресс доставка KEY', 'Экспресс доставка VALUE')]


class OrderDeliveryForm(forms.Form):
    delivery_type = forms.ChoiceField(widget=forms.RadioSelect(),
                                      choices=ORDER_DELIVERY_TYPE_SELECT)
    city = forms.CharField(required=True)
    address = forms.CharField(required=True)


ORDER_PAYMENT_TYPE_SELECT = [('Онлайн картой KEY', 'Онлайн картой VALUE'),
                             ('Онлайн со случайного чужого счета KEY', 'Онлайн со случайного чужого счета VALUE')]


class OrderPaymentForm(forms.Form):
    payment_type = forms.ChoiceField(widget=forms.RadioSelect(),
                                     choices=ORDER_PAYMENT_TYPE_SELECT)


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class OrderRegistryForm(forms.Form):
    fio = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                       'placeholder': 'Введите ФИО'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                 'placeholder': 'Введите номер телефона'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                          'placeholder': 'Введите e-mail'}))
    password1 = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": 'form-input',
                                          "placeholder": "Введите пароль"}),
        strip=False,
    )
    password2 = forms.CharField(
        required=True,
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": "form-input",
                                          "placeholder": "Введите пароль повторно"})
    )


class AccountForm(forms.Form):
    account = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-input Payment-bill",
                                                                           "id": "numero1",
                                                                           "name": "numero1",
                                                                           "type": "text",
                                                                           "placeholder": "9999 9999",
                                                                           "data-mask": "9999 9999",
                                                                           "data-validate": "require pay"}))
