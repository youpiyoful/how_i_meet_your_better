from django import forms


class RegistrationForm(forms.Form):
    firstname = forms.CharField(
        # label="prénom",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'firstname',
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
                'name': 'lastname',
                'id': 'lastname',
                'aria-describedby': 'inputLastname'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'name': 'email',
                'class': 'form-control',
                'id': 'inputEmail',
                'aria-describedby': 'inputEmail'
            }
        )
    )

    password_field = forms.CharField(max_length=32, widget=forms.PasswordInput(
        attrs={
            'name': 'password',
            'class': 'form-control',
            'id': 'inputPassword1'
        }
    ))

# TODO faire le form pour la connexion

# class LoginForm