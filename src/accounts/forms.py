import django
import json
import urllib
import urllib.request
from blog import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()


class UserLoginForm(django.forms.Form):
    username = django.forms.CharField()
    password = django.forms.CharField(widget=django.forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise django.forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise django.forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise django.forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(django.forms.ModelForm):
    email = django.forms.EmailField(label='Email address')
    # email2 = forms.EmailField(label='Confirm Email')
    password = django.forms.CharField(widget=django.forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            # 'email2',
            'password'
        ]

    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get('email')
    #     email2 = self.cleaned_data.get('email2')
    #     if email != email2:
    #         raise forms.ValidationError("Emails must match")
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("This email has already been registered")

    #     return super(UserRegisterForm,self).clean(*args, **kwargs)
