from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio']  # Include bio field

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
