from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image","quantity"]
        
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }
        
        


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity']
        
        
    quantity = forms.IntegerField(
        min_value=0,
        label="Update Stock Quantity",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new stock quantity'
        })
    )
    
    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        return qty