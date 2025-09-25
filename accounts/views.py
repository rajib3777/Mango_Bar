from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.models import Group
from accounts.models import CustomUser, SellerProfile, CustomerProfile
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
from orders.models import OrderItem
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import FormView
from datetime import timedelta
from django.utils.timezone import now
from .decorators import role_required
from django.db.models.functions import TruncMonth
from django.db.models import F
from .forms import StockUpdateForm, ProductQuickForm
from cart.models import Cart,CartItem
from .forms import UserUpdateForm, CustomerProfileForm, ResetPasswordForm
from .models import CustomerProfile, SellerProfile
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomRegistrationForm


def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                
                role = form.cleaned_data.get('role')
                if role == "Seller":
                    group, _ = Group.objects.get_or_create(name='Seller')
                else:
                    group, _ = Group.objects.get_or_create(name='Customer')
                user.groups.add(group)
                
                
                try:
                       
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    
                    activation_link = request.build_absolute_uri(
                        reverse_lazy('activate-user', kwargs={'uidb64': uid, 'token': token})
                    )
                    
                    subject = 'Activate your Mango Bar account'
                    message = render_to_string('accounts/activation_mail.html', {
                        'user': user,
                        'activation_link': activation_link,
                    })

                    email = EmailMultiAlternatives(subject, '', to=[user.email])
                    email.attach_alternative(message, 'text/html')
                    email.send()

                    messages.success(request, 'A confirmation mail has been sent. Please check your email.')
                    return redirect('sign-in')

                except Exception as e:
                    print("❌ Email sending failed:", e)
                    user.delete()
                    messages.error(request, 'Signup failed because activation mail could not be sent. Try again or contact admin.')
                    return redirect('sign-up')

            except Exception as e:
                print("❌ Error during signup:", e)
                messages.error(request, f"Something went wrong: {e}")
                return render(request, 'accounts/register.html', {"form": form})

        else:
            print("❌ Form errors:", form.errors)
            return render(request, 'accounts/register.html', {"form": form})
        
    return render(request, 'accounts/register.html', {"form": form})

    




@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')

def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
        
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        from .models import CustomerProfile, SellerProfile
        if user.role == 'Customer':
            CustomerProfile.objects.get_or_create(user=user)
        elif user.role == 'Seller':
            SellerProfile.objects.get_or_create(user=user)


        messages.success(request, "Your account has been activated. You can now log in.")
        return redirect('sign-in')
    
    else:
        messages.error(request, "Your account activation link is invalid or has expired.")
        return redirect('sign-up')
    

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if not user.is_active:
                messages.error(request, "Your account is not activated yet. Please check your email for activation link.")
                return render(request, 'accounts/login.html', {'form': form})

            login(request, user)
            if user.is_superuser:
                return redirect('admin-dashboard')
            elif user.groups.filter(name='Seller').exists():
                return redirect('seller-dashboard')
            else:
                return redirect('customer-dashboard')
            
            
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'accounts/login.html', {'form': form})
    

    
@login_required
@role_required('Admin')
def admin_dashboard(request):
    
    monthly = (
        OrderItem.objects
        .annotate(month=TruncMonth('order__created_at'))
        .values('month')
        .annotate(total=Sum(F('quantity') * F('price_per_item')))
        .order_by('month')
        
    )
    
    chart_labels = [m['month'].strftime("%b %Y") if m['month'] else 'Unknown' for m in monthly]
    chart_values = [float(m['total'] or 0) for m in monthly]
    
    products = Product.objects.all().select_related('seller')
    sellers = CustomUser.objects.filter(role="Seller")
    customers = CustomUser.objects.filter(role="Customer")
    
    stock_form = StockUpdateForm()
    quick_form = ProductQuickForm()
    
    if request.method == "POST" and 'update_stock' in request.POST:
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = Product.objects.get(id=product_id)
            product.quantity += quantity
            product.save()
            messages.success(request, "Stock updated successfully.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Please correct the errors in stock update form.")
            stock_form = form
    
    context = {
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "products": products,
        "sellers": sellers,
        "customers": customers,
        "stock_form": stock_form,
        "quick_form": quick_form,
    }
    
    return render(request, "accounts/admin_dashboard.html", context)



@login_required
@role_required('Seller')
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    
    quick_form = ProductQuickForm()
    stock_form = StockUpdateForm()
    
    if request.method == "POST":
        if "quick_create" in request.POST:
            quick_form = ProductQuickForm(request.POST, request.FILES)
            if quick_form.is_valid():
                product = quick_form.save(commit=False)
                product.seller = request.user
                product.save()
                messages.success(request, "Product created successfully.")
                return redirect("seller-dashboard")
            else:
                messages.error(request,"Please correct the errors in product form.")
                
        elif "update_stock" in request.POST:
            stock_form = StockUpdateForm(request.POST)
            if stock_form.is_valid():
                product_id = request.POST.get("product_id")
                product = get_object_or_404(Product, id=product_id, seller=request.user)
                delta = stock_form.cleaned_data["delta"]
                product.stock += delta
                product.save()
                messages.success(request, "Stock updated successfully.")
                return redirect("seller-dashboard")
            else:
                messages.error(request, "Invalid stock update form.")
                
    context = {
        "products": products,
        "quick_form": quick_form,
        "stock_form": stock_form,
    }
    return render(request, "accounts/seller_dashboard.html", context)



@login_required
@role_required('Admin','Seller','Customer')
def customer_dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    thirty_days_ago = now() - timedelta(days=30)
    new_orders = [o for o in orders if o.created_at >= thirty_days_ago]
    previous_orders = [o for o in orders if o.created_at < thirty_days_ago]
    
    def order_total(o):
        return sum([item.quantity * float(item.price_per_item) for item in o.items.all()])
    
    context = {
        "new_orders": new_orders,
        "previous_orders": previous_orders,
        "order_total": order_total,
    }
    return render(request, "accounts/customer_dashboard.html", context)


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
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

class EditprofileView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = CustomUser
    form_class = Profileupdateform
    template_name = 'accounts/edit_profile.html' 
    success_url = reverse_lazy('profile')
    success_message = "Profile update Successfully"
    
    def get_object(self):
        return self.request.user

    
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=user_email)

                # 🔑 Token তৈরি
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # 🔗 Reset link বানানো
                reset_link = request.build_absolute_uri(
                    reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )

                # 📧 ইমেইল তৈরি
                subject = 'Reset your password'
                message = render_to_string('accounts/password_reset_mail.html', {
                    'user': user,
                    'reset_link': reset_link,
                })

                mail = EmailMultiAlternatives(subject, '', to=[user.email])
                mail.attach_alternative(message, 'text/html')
                mail.send()

                messages.success(request, '✅ Password reset link sent to your email.')
                return redirect('sign-in')

            except CustomUser.DoesNotExist:
                messages.error(request, '❌ No user found with this email address.')
    else:
        form = ResetPasswordForm()

    return render(request, 'accounts/password_reset_form.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    return redirect('sign-in')
                else:
                    messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/password_reset_confirm.html', {'user': user})
            
        else:
            messages.error(request, 'Invalid token or user ID.')
            return redirect('reset_password')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('reset_password')
    


@login_required
def edit_profile(request):
    
    profile,created = SellerProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        print("FILES:", request.FILES)
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = CustomerProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "✅ Profile updated successfully!")

            return redirect("user_profile", user_id=request.user.id)
        else:
            print("❌ User form errors:", user_form.errors)
            print("❌ Profile form errors:", profile_form.errors)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = CustomerProfileForm(instance=profile)
        
    return render(request, "accounts/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })
\


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
    


@login_required
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    profile = None
    orders = None
    products = None
    total_spent = 0
    total_earned = 0

    if user.role == "Customer":
        profile = getattr(user, "customer_profile", None)
        template = "accounts/customer_profile.html"

        orders = Order.objects.filter(user=user).prefetch_related("items__product")
        
        for order in orders:
            for item in order.items.all():
                total_spent += item.product.price * item.quantity
                
                
    elif user.role == "Seller":
        profile = getattr(user, "seller_profile", None)
        template = "accounts/seller_profile.html"

        products = Product.objects.filter(seller=user)

        seller_items = OrderItem.objects.filter(product__seller=user)
        for item in seller_items:
            total_earned += item.product.price * item.quantity
            
            

    elif user.role == "Admin":
        profile = getattr(user, "admin_profile", None)
        template = "accounts/admin_profile.html"
        
        products = Product.objects.filter(seller=user)
        
        seller_items = OrderItem.objects.filter(product__seller=user)
        for item in seller_items:
            total_earned += item.product.price * item.quantity

    context = {
        "profile_user": user,
        "profile": profile,
        "orders": orders,
        "products": products,
        "total_spent": total_spent,
        "total_earned": total_earned,
    }

    return render(request, template, context)
