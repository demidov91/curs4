from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class UserCustomAdminCreationForm(UserCreationForm):
    username = forms.EmailField(label="Email", max_length=254)


class UserCustomAdminChangeForm(UserChangeForm):
    username = forms.EmailField(label="Email", max_length=254)