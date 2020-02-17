from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from .models import CustomUser
User = get_user_model()

class USerLoginForm(forms.Form):
    username= forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")



        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("This user does not exist")

            if not user.check_password(password):
                return forms.ValidationError("Incorrect Password")

            if not user.is_active:
                raise forms.ValidationError("This user dis no longer active")


        return super(USerLoginForm, self).clean(*args, **kwargs)



class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm,self).__init__(*args, **kargs)
        del self.fields['username']

        class Meta:
            model = CustomUser
            fields=('email',)


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm,self).__init__(*args, **kargs)
        del self.fields['username']

        class Meta:
            model = CustomUser