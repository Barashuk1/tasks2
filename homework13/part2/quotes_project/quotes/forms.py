from django import forms
from .models import Quote
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class AddQuoteForm(forms.ModelForm):
    author_name = forms.CharField(label='Ім\'я автора', required=True)
    quote_text = forms.CharField(label='Текст цитати', widget=forms.Textarea, required=True)
    tags = forms.CharField(label='Теги (через кому)', required=False)

    class Meta:
        model = Quote
        fields = ['author_name', 'quote_text', 'tags']