from django import forms
from .models import ShippingAddress


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'phone', 'city', 'address', 'postal_code']