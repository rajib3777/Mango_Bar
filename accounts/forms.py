from django import forms
from accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
        
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    
    )


    class Meta:
        model = CustomUser
        fields = ['email', 'role', 'address', 'phone', 'shop_name']


        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}),
            'shop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name (only for sellers)'}),
        
        }
    def clean_shop_name(self):
        role = self.cleaned_data.get('role')
        shop_name = self.cleaned_data.get('shop_name')
        if role == 'Seller' and not shop_name:
            raise forms.validationError("Shop name is required for sellers.")
        return shop_name
        
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
        
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'address', 'phone', 'shop_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'shop_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

