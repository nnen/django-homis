from django import forms


class LogInForm(forms.Form):
    username = forms.CharField(min_length = 0, required = False)
    password = forms.CharField(min_length = 0, required = False)

