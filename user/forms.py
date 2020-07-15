from django import forms


class RegistrationForm(forms.Form):
    firstname = forms.CharField(
        # label="prénom",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'firstname',
                'aria-describedby': 'inputFirstname'
            }
        )
    )
    lastname = forms.CharField(
        # label="nom",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lastname',
                'aria-describedby': 'inputLastname'
            }
        )
    )
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput())

# TODO faire le form pour la connexion

# class LoginForm