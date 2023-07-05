from django import forms
from .models import UserSuggest


class UserSuggestForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    subject = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = UserSuggest
        fields = ['username', 'email', 'subject', 'text']
