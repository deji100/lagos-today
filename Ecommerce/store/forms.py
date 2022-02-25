from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm, PasswordResetForm, UserCreationForm)

from .models import *


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username', 'autofocus':True}), label='Username')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}), label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}), label='Confirm password')

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2']


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Enter current password'}), label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Enter new password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Confirm new password'}), label='Confirm Password')

    class Meta:
        model = Account
        fields = ['old_password', 'new_password1', 'new_password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type':'email', 'placeholder': 'Enter email', 'autofocus':True}), label='Email')

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Enter password'}), label='Password')

    class Meta:
        model = Account
        fields = ['username', 'password']
