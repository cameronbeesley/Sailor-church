from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from phonenumber_field.formfields import SplitPhoneNumberField
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone_number = SplitPhoneNumberField()
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'surname', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    phone_number = SplitPhoneNumberField()
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'surname', 'phone_number')