from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser




class CustomRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('Customer','Customer'),
        ('Seller','Seller'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    
    security_pass = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        help_text="Required only if you sign up as Seller"
    )
    
    password1 = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',
                  'email','role','security_pass',
                  'password1', 'confirm_password',]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = CustomUser.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password1):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password1):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password1):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password1):
            errors.append(
                'Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return password1

    def clean(self):  # non field error
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        role = cleaned_data.get('role')
        security_pass = cleaned_data.get('security_pass')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Password do not match")
        
        if role == 'Seller':
            admin_username = 'rajib3777'
            if security_pass != admin_username:
                raise forms.ValidationError("Invalid security pass for Seller")

        return cleaned_data
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'block w-full px-4 py-2 mt-2 text-black bg-white border border-black rounded-md focus:border-blue-500 focus:outline-none focus_ring'
            })
            
class Profileupdateform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'role','contact_number','profile_picture']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'block w-full px-4 py-2 mt-2 text-black bg-white border border-black rounded-md focus:border-blue-500 focus:outline-none focus_ring'
            })
    

    
    
    