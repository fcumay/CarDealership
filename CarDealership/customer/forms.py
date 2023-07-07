from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from django_countries.fields import CountryField


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class SignUpForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))
    location = CountryField().formfield(
        widget=forms.Select(attrs={"class": "form-control"})
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Customer
        fields = (
            "name",
            "email",
            "location",
            "contact_number",
            "password1",
            "password2",
        )
