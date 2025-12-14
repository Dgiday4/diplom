from django import forms
from django.contrib.auth import authenticate
from .models import User


class LoginForm(forms.Form):
    login = forms.CharField(label='логин')
    password = forms.CharField(label='пароль', widget =forms.PasswordInput())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)


    def get_user(self):
        return self.user


    def clean(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']
        self.user = authenticate(self.request, username=login, password=password)

        if not self.user:
            raise forms.ValidationError('неверный логин или пароль')

        return self.cleaned_data


class RegisterForm(forms.Form):
    login = forms.CharField(label='логин')
    password_1 = forms.CharField(widget=forms.PasswordInput,label  = 'пароль')
    password_2 = forms.CharField(widget=forms.PasswordInput, label='повтор пароля')
    first_name = forms.CharField(label='имя', required=False)
    last_name = forms.CharField(label='фамилия', required=False)

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError('такой пользователь уже есть')
        return login

    def clean(self):
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']

        if password_1 != password_2:
            raise forms.ValidationError('пароли не совпадают')

        return self.cleaned_data
