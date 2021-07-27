from django.db.models.base import ModelState
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Profile
from .decorators.auth import unauthenticated_user
from .helpers import send_forgetPassword_token_mail, send_registration_token_mail, generate_token
# Create your views here.

@login_required(login_url='/login/')
def home(request):
    """ print(request.session) 
    print(request.session.items())
    print("Id: ",request.session['_auth_user_id']) """
    if request.session.has_key('customer_id'):
        print("Home: ", request.session['customer_id']) 
    return render(request, 'account/home.html')


@unauthenticated_user
def register(request):
    if request.method=='POST':
        # getting data
        username = request.POST.get('username').strip()
        email = request.POST.get('email')
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip() 

        # validating fields
        if username=="" or email=="" or password1=="" or password2=="":
            messages.success(request, 'Invalid empty fields.')
            return redirect('register')
        if User.objects.filter(username__iexact = username).first():
            messages.success(request, 'Username is already taken.')
            return redirect('register')
        if User.objects.filter(email__iexact = email).first():
            messages.success(request, "Email is already taken.")
            return redirect('register')
        if password1 != password2:
            messages.success(request, "Password is not matching.")
            return redirect('register')

        user_obj = User(username = username, email=email)
        user_obj.set_password(password1)
        user_obj.save()
        auth_token = generate_token()
        profile_obj = Profile.objects.create(user = user_obj, auth_token=auth_token)
        profile_obj.save()
        send_registration_token_mail(username, email, auth_token)
        return render(request, 'account/token.html')
    else:
        return render(request, 'account/register.html')

def verify_token(request, token):
    profile_obj = Profile.objects.filter(auth_token__iexact=token).first()
    if profile_obj is None:
        messages.success(request, 'Invalid token !!!')
        return redirect('error')
    profile_obj.is_verified = True
    profile_obj.save()
    messages.success(request, "Account verified successfully.")
    return redirect('login')

@unauthenticated_user
def login_user(request):
    if request.method=='POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        if username=="" or password=="":
            messages.warning(request, "Invalid empty fields !!!")
            return redirect('login')
        
        user_obj = User.objects.filter(username__exact = username).first()
        if user_obj is None:
            messages.success(request, "Invalid username.")
            return redirect('login')
        
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'User is not verified. Please check you mail.')
            return redirect('login')
        user = authenticate(username = username, password=password)
        if user is None:
            messages.success(request, 'Invalid password !!!')
            return redirect('login')
        request.session['customer_id'] = user.id 
        print("Login: ",request.session['customer_id'])
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account/login.html')

def logout_user(request):
    logout(request)
    print("LOgout: ",request.session.get('customer_id'))
    return redirect('login')

def error_page(request):
    return render(request,"account/error.html")

""" Forget Password Part """
def forgetPassword(request):
    if request.method=='POST':
        email = request.POST.get('email')
        if email=="":
            messages.success(request, "Empty email field.")
            return render(request, 'account/forget_password.html')
        user_obj = User.objects.filter(email__iexact = email).first()
        if user_obj is None:
            messages.success(request, "User with the email doesn't exist. Please! write valid email.")
            return render(request, 'account/forget_password.html')
        profile_obj = Profile.objects.get(user = user_obj)
        forget_password_token = generate_token()
        profile_obj.forget_password_token = forget_password_token
        profile_obj.save()
        print('Forget token: ', forget_password_token)
        send_forgetPassword_token_mail(email, forget_password_token)
        messages.success(request, 'A link is sent to your email. Please! check your email.')
        return redirect('forget-password')
    else: 
        return render(request, 'account/forget_password.html')

def changePassword(request, token):
    profile_obj = Profile.objects.filter(forget_password_token__iexact=token).first()
    if profile_obj is None:
        messages.success(request, 'Token error.')
        return redirect('error') 
    
    if request.method=='POST':
        p1 = request.POST.get('password1').strip()
        p2 = request.POST.get('password2').strip()
        if p1=="" or p2=="":
            messages.success(request, "Fields cannot be empty!!!")
            return render(request, 'account/change_password.html')
        elif p1!=p2:
            messages.success(request, 'Password does not match.')
            return render(request, 'account/change_password.html')

        user_obj = profile_obj.user
        user_obj.set_password(p1)
        user_obj.save()
        messages.success(request, 'Password changed successfully.')
        return redirect('login')
    else:
        return render(request, 'account/change_password.html')
      
