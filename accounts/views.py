from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.models import Group
from accounts.models import CustomUser
from django.contrib.auth import login, authenticate, logout
from accounts.forms import CustomRegistrationForm 
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import AuthenticationForm as LoginForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Count
from products.models import Product
from orders.models import Order
from django.db.models import Count, Sum
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from accounts.forms import Profileupdateform
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash

from django.db.models import Q
from orders.models import CartItem, OrderItem
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import FormView
 


# Create your views here.


def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        print("📥 Received POST request for signup")
        form = CustomRegistrationForm(request.POST)
        print("✅ Form validity:", form.is_valid())
        if form.is_valid():
            try:
                print("Yes form is valid")
            except Exception as e:
                print("❌ Email error:", e)
                
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False   
            user.save()
                     
            role = form.cleaned_data.get('role')
            
            if role == 'Seller':
                group, _ = Group.objects.get_or_create(name='Seller')
            else:
                group, _ = Group.objects.get_or_create(name='Customer')
                
                
            user.groups.add(group)
                

            #token
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            #activation_link
            
            activation_link = request.build_absolute_uri(
                reverse_lazy('activate-user', kwargs={'uidb64':uid,'token':token})
            )
            
            

            
            #actiavtion mail
            subject = 'Activate your Mango Bar account'
            message = render_to_string('accounts/activation_mail.html',{
                'user' : user,
                'activation_link' : activation_link,
            })
            
            email = EmailMultiAlternatives(subject,'',to=[user.email])
            email.attach_alternative(message,'text/html')
            email.send()
            print("✅ Activation email sent to:", user.email)

                        
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')

        else:
            print("Form is not valid")
           
            print("❌ Form invalid:", form.errors)

    return render(request, 'accounts/register.html', {"form": form})


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Seller').exists():
                return redirect('seller-dashboard')
            else:
                return redirect('customer-dashboard')
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')


def activate_user(request, uidb64 , token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except CustomUser.DoesNotExist:
        return HttpResponse('User not found')
    
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    products = Product.objects.all()
    total_products = products.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    

    context = {
        'products' : products,
        'total_products' :total_products,
        'total_orders' : total_orders,
        'total_revenue' : total_revenue,
        
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Seller').exists())
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    total_products = products.count()
    total_orders = Order.objects.filter(seller=request.user).count()
    total_revenue = Order.objects.filter(seller=request.user).aggregate(total=Sum('total_amount'))['total'] or 0
    
    return render(request,'accounts/seller_dashboard.html', {
        'products': products,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    })


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Customer').exists())
def customer_dashboard(request):
    products = Product.objects.all()
    total_products = products.count()
    total_orders = Order.objects.filter(customer=request.user).count()                                                                          
    return render(request,'accounts/customer_dashboard.html',{
        'products': products,
        'total_products': total_products,
        'total_orders': total_orders,
    })



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Customer').exists())
def profile_view(request):
    user = request.user
    orders = Order.objects.filter(customer=user)
    context = {
        'user': user,
        'orders': orders,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Customer').exists())
def my_orders(request):
    orders = Order.objects.filter(customer=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

class Editprofileview(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = CustomUser
    form_class = Profileupdateform
    template_name = 'accounts/edit_profile.html' 
    success_url = reverse_lazy('profile')
    success_message = "Profile update Successfully"
    
    def get_object(self):
        return self.request.user

    
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            email = EmailMultiAlternatives(subject, '', to=[user.email])
            email.attach_alternative(message, 'text/html')
            email.send()
            messages.success(request, 'Password reset link sent to your email.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    return render(request, 'accounts/reset_password.html')

def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                
                if new_password == confirm_password:
                    user = user.objects.get(id=uid)
                    user.set_password(new_password)
                    user.save()
                    return redirect('sign-in')
                else:
                    messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_confirm.html', {'user': user})
            
        else:
            messages.error(request, 'Invalid token or user ID.')
            return redirect('reset-password')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('reset-password')
    
    
class EditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = Profileupdateform
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')
    success_message = "Profile updated successfully"

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')
    success_message = "Password changed successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
