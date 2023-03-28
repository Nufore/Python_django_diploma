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
    delivery_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onchange': "set_delivery_checked()"}),
                                      choices=ORDER_DELIVERY_TYPE_SELECT)
    city = forms.CharField(required=True)
    address = forms.CharField(required=True)


ORDER_PAYMENT_TYPE_SELECT = [('Онлайн картой KEY', 'Онлайн картой VALUE'),
                             ('Онлайн со случайного чужого счета KEY', 'Онлайн со случайного чужого счета VALUE')]


class OrderPaymentForm(forms.Form):
    payment_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onchange': "set_payment_checked()"}),
                                     choices=ORDER_PAYMENT_TYPE_SELECT)

