from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                print('FIRST')
                raise forms.ValidationError('Этого пользователя не существует')
            if not user.check_password(password):
                print('SECOND')

                raise forms.ValidationError('Неверный пароль')
            if not user.is_active:
                raise forms.ValidationError('Этот пользователь хуй')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class IndexForm(forms.Form):
    post = forms.CharField
