from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) 
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user = authenticate(request=self.request, username=email, password=password)  
            if self.user is None:
                raise forms.ValidationError(
                    _("Invalid email or password"),
                    code='invalid_login',
                )
        return self.cleaned_data

    def get_user(self):
        return self.user
