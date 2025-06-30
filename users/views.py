from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .decorators import login_required

# Create your views here.

@login_required
def profile(request):
    # username = request.session.get('username', 'Guest')  # fallback if not logged in
    user = request.user

    if request.method == 'POST':
        phone = request.POST.get('phonenumber')
        addr = request.POST.get('address')
        password = user.password if not request.POST.get('new-password') else make_password(request.POST.get('new-password'))

        user.phonenumber = phone
        user.address = addr
        user.password = password
        user.save()

        messages.success(request, 'Update user infomation successfully!')
        return redirect('user:profile')

    return render(request, 'components/profile.html', {'user': user})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects(username=username).first()

        if not user:
            messages.error(request, 'User not found!')
            return redirect('user:signin')
        
        if not check_password(password, user.password):
            messages.error(request, 'Incorrect password!')
            return redirect('user:signin')
        
        request.session['username'] = username
        request.session['logged_in'] = True
        return redirect('home')
        
    return render(request, 'components/signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm-password')
        phone = request.POST.get('phone')

        print(username)
        print(password)
        print(confirm_pass)
        print(phone)

        if User.objects(username=username).first():
            messages.error(request, 'User alrealy exist!')
            return redirect('user:signup')
        
        if password != confirm_pass:
            messages.error(request, 'Password not match!')
            return redirect('user:signup')
        
        hashed_pass = make_password(password)
        user = User(
            username=username,
            password=hashed_pass,
            phonenumber=phone
        )

        user.save()
        messages.success(request, 'Register new user successfully!')
        return redirect('user:signin')

    return render(request, 'components/signup.html')

def signout(request):
    request.session.flush()
    return redirect('home')