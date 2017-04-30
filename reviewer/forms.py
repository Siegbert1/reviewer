from django import forms
from .models import Progress
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', )


#class ProgressForm(forms.ModelForm):

    #class Meta:
        #model = Progress
        #fields = ('progress',)
