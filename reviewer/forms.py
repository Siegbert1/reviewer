from django import forms
from .models import Progress, Case_ZR
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', )


class CaseForm_ZR(forms.ModelForm):

    class Meta:
        model = Case_ZR
        fields = ('title', 'category', 'text', 'explanation', 'public', 'kv', 'p', 'mangel', 'p2', 'gefahruebergang', 'p3',)

    def process(self):
    # Assumes .cleaned_data exists because this method is always invoked after .is_valid(), otherwise will raise AttributeError
        cd = self.cleaned_data
    # do something interesting with your data in cd
        string = ""
        for key, value in cd.items():
            if key == "title" or key == "category" or key == "text" or key == "explanation" or key == "public":
                pass
            else:
                if value == True:
                    string = string + "T"
                else: # value == False
                    string = string + "F"

        self.cleaned_data['string'] = string


class CheckForm_ZR(forms.ModelForm):
    class Meta:
        model = Case_ZR
        fields = ('kv', 'p', 'mangel', 'p2', 'gefahruebergang', 'p3',)


    def process(self):
    # Assumes .cleaned_data exists because this method is always invoked after .is_valid(), otherwise will raise AttributeError
        cd = self.cleaned_data
    # do something interesting with your data in cd
        string = ""
        for key, value in cd.items():
            if key == "title" or key == "category" or key == "text" or key == "explanation" or key == "public":
                pass
            else:
                if value == True:
                    string = string + "T"
                else: # value == False
                    string = string + "F"

        self.cleaned_data['answer_string'] = string
