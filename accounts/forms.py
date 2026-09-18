from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

CTRL = {'class': 'form-control'}


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=CTRL), min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=CTRL), label='Confirm password')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={**CTRL, 'placeholder': 'Ahmed'}),
            'last_name': forms.TextInput(attrs={**CTRL, 'placeholder': 'Ali'}),
            'email': forms.EmailInput(attrs={**CTRL, 'placeholder': 'you@mail.com'}),
            'phone': forms.TextInput(attrs={**CTRL, 'placeholder': '01012345678'}),
        }

    def clean_email(self):
        # Req 3: friendly message instead of a raw DB error page.
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered. Try logging in instead.')
        return email

    def clean(self):
        data = super().clean()
        # Req 4: confirmation must match
        if data.get('password') != data.get('confirm_password'):
            raise forms.ValidationError('Password confirmation does not match.')
        return data


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={**CTRL, 'placeholder': 'you@mail.com'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=CTRL))


class CustomUserCreationForm(UserCreationForm):
    """For Django Admin add-user page (no username, email login)."""

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone')
