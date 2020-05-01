from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
        help_texts = {
            'username':None
        }
        widgets = {
            'password':forms.PasswordInput()
        }
