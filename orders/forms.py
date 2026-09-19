from django import forms
from .models import Order
from accounts.models import normalize_egyptian_phone

CTRL = {'class': 'form-control'}


class CheckoutForm(forms.ModelForm):
    def clean_phone(self):
        # Same strict Egyptian rule as registration; stored normalized.
        return normalize_egyptian_phone(self.cleaned_data.get('phone', ''))

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
