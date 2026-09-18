from django import forms
from .models import Order

CTRL = {'class': 'form-control'}


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city']
        widgets = {
            'full_name': forms.TextInput(attrs={**CTRL, 'placeholder': 'Ahmed Ali'}),
            'email': forms.EmailInput(attrs={**CTRL, 'placeholder': 'you@mail.com'}),
            'phone': forms.TextInput(attrs={**CTRL, 'placeholder': '01012345678'}),
            'address': forms.TextInput(attrs={**CTRL, 'placeholder': 'Street, building, apartment'}),
            'city': forms.TextInput(attrs={**CTRL, 'placeholder': 'Cairo'}),
        }
