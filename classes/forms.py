from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        error_messages = {'name': {'required': 'Product name is required'}}
        help_text = {'name': 'Enter product name'}

class CartItem(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['user', 'product', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'receiver_name', 'address', 'mobile', 'payment_option']
        widgets = {
            'mobile': forms.TextInput(attrs={'pattern':'[0-9]{10}'}),
        }
