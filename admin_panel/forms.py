from django import forms
from products.models import Mango


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Mango
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