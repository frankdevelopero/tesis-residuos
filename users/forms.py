from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(
        label="Correo electrónico",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico',
                'type': 'email',
                'required': 'true',
            }
        )
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
                'required': 'true',
            }
        )
    )
