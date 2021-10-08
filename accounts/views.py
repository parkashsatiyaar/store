from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import RegistrationForm, UserForm, UserProfileForm
from accounts.models import Account, UserProfile
from django.contrib.auth.models import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from app.models import Home
from cart.models import Cart, CartItem
from cart.views import _getCartId
from orders.models import Order, OrderProduct
# Create your views here.


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = Account.objects.filter(email=email)
                username = email.split("@")[0]
                user = Account.objects.create_user(
                    first_name=first_name, last_name=last_name,  email=email, password=password, username=username)
                user.phone_number = phone_number
                user.save()
                profile = UserProfile()
                profile.user_id = user.id
                profile.profile_picture = "default/default.png"
                profile.save()
                current_site = get_current_site(request)
                mail_subject = "Account Email Activation Email"
                html_content = render_to_string('store/accountEmailVarification.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                text_content = strip_tags(html_content)
                send_mail = send_mail = EmailMultiAlternatives(
                    mail_subject,
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                send_mail.attach_alternative(html_content, 'text/html')
                send_mail.send()
                request.session['confirm_email'] = email
                return redirect('confirm')
            else:
                messages.info(request, 'Email already exist!')

        form = RegistrationForm()
        home = Home.objects.all()
        context = {
            'homes': home,
            'form': form
        }
        return render(request, "store/signup.html", context)


def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if not request.session.get('next_url'):
            request.session['next_url'] = request.GET.get('next')
        url = request.session.get('next_url')
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                try:
                    cart = Cart.objects.get(cartId=_getCartId(request))
                    iscartItem = CartItem.objects.filter(cart=cart).exists()
                    if iscartItem:
                        cartItem = CartItem.objects.filter(cart=cart)
                        for item in cartItem:
                            item.user = user
                            item.save()
                except:
                    pass
                auth.login(request, user)
                if url == "/checkout":
                    return redirect('cart')
                elif url:
                    return HttpResponseRedirect(url)
                else:
                    return redirect('dashboard')
            else:
                messages.info(request, 'Invalid email or password!')
                return redirect('signin')
        home = Home.objects.all()
        context = {
            'homes': home,
        }
        return render(request, "store/signin.html", context)


def confirm(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.session.get('confirm_email'):
        request.session['confirm_email'] = None
        return render(request, "store/afteremailsending.html")
    else:
        return redirect('home')


@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    return redirect('signin')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('signin')
    else:
        return redirect('signup')


@login_required(login_url='signin')
def dashboard(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    home = Home.objects.all()
    orders = Order.objects.order_by(
        '-created_date').filter(user=request.user, is_ordered=True)
    orders_count = orders.count()
    if not "dashboard" in request.path:
        return redirect('dashboard')
    context = {
        'homes': home,
        'orders_count': orders_count,
        'userprofile': userprofile
    }
    return render(request, "store/dashboard.html", context)


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            current_site = get_current_site(request)
            mail_subject = "Change Password Verification"
            html_content = render_to_string('store/passwordChange.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            text_content = strip_tags(html_content)
            send_mail = send_mail = EmailMultiAlternatives(
                mail_subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [email]
            )
            send_mail.attach_alternative(html_content, 'text/html')
            send_mail.send()
            request.session['confirm_email'] = email
            return redirect('confirm')
        else:
            return redirect('signin')
    return render(request, "store/forgotPassword.html")


def resetPasswordValidation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetPassword')
    else:
        return redirect('signin')


def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        con_password = request.POST['con_password']
        if password == con_password:
            try:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                return redirect('signin')
            except:
                redirect('signin')
        else:
            return redirect('resetPassword')
    return render(request, 'store/resetForm.html')


@login_required(login_url="signin")
def my_orders(request):
    home = Home.objects.all()
    orders = Order.objects.filter(
        user=request.user, is_ordered=True).order_by('-created_date')
    context = {
        'orders': orders,
        'homes': home
    }
    return render(request, 'store/my_orders.html', context)


@login_required(login_url="signin")
def edit_profile(request):
    home = Home.objects.all()
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST,
                             instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('edit_profile')
        else:
            redirect('dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
        'homes': home
    }
    return render(request, 'store/edit_profile.html', context)


@login_required(login_url="signin")
def change_password(request):
    home = Home.objects.all()
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        user = Account.objects.get(username__exact=request.user.username)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
        return redirect('change_password')
    context = {
        'homes': home
    }
    return render(request, 'store/change_password.html', context)


@login_required(login_url="signin")
def order_details(request, order_id):
    home = Home.objects.all()
    try:
        order_detail = OrderProduct.objects.filter(
            order__order_number=order_id)
        order = Order.objects.get(order_number=order_id)
        subtotal = 0
        for i in order_detail:
            subtotal += i.product_price * i.quantity
        context = {
            'homes': home,
            'order_detail': order_detail,
            'order': order,
            'subtotal': subtotal,
        }
        return render(request, "store/order_details.html", context)
    except:
        return redirect('my_orders')
