from django import forms


class RegistrationForm(forms.Form):
    firstname = forms.CharField(label='firstname')

