from django import forms


class BaseForm(forms.Form):
    """modele form for connection"""
    email = forms.EmailField(
        # label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'inputEmail1',
                'aria-describedby': 'inputEmail'
            }
        )
    )

    password_field = forms.CharField(
        max_length=32,
        # label='Adresse mail',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'inputPassword1'
            }
        )
    )


class RegistrationForm(BaseForm):
    """model form for register"""
    firstname = forms.CharField(
        # label="Prénom",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'firstname',
                'aria-describedby': 'inputFirstname'
            }
        )
    )
    lastname = forms.CharField(
        # label="Nom",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lastname',
                'aria-describedby': 'inputLastname'
            }
        )
    )


# TODO faire le form pour la connexion

# class LoginForm