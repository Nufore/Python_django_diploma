from django import forms
from .models import Feedback


class ReviewAddForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-textarea',
                                                                        'placeholder': 'Review'}))

    class Meta:
        model = Feedback
        fields = ('text',)
