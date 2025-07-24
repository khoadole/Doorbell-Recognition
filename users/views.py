from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User, OtpToken
from .decorators import login_required
from .utils import sendOtp
from datetime import datetime
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
        email = request.POST.get('email')

        # print(username)
        # print(password)
        # print(confirm_pass)
        # print(email)

        if User.objects(username=username).first():
            messages.error(request, 'User alrealy exist!')
            return redirect('user:signup')
        
        if password != confirm_pass:
            messages.error(request, 'Password not match!')
            return redirect('user:signup')
        
        if User.objects(email=email).first():
            messages.error(request, 'Email alrealy exist!')
            return redirect('user:signup')
        
        hashed_pass = make_password(password)
        
        user = User(
            username=username,
            password=hashed_pass,
            email=email
        )

        user.save()
        messages.success(request, 'Register new user successfully!')
        return redirect('user:signin')

    return render(request, 'components/signup.html')

def signout(request):
    request.session.flush()
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if email exists in database
        if not User.objects(email=email).first():
            messages.error(request, "Email doesn't exist in database!")
            return redirect('user:forgot_password')

        # If email exists, continue with sending OTP or reset logic
        messages.success(request, "OTP sent to your email.")
        user = User.objects(email=email).first()
        request.session['reset_email'] = email
        sendOtp(user)
        # return redirect('user:reset_password')
        return render(request, 'components/reset_password.html', {
                'email': email
            })

    return render(request, 'components/forgot_password.html')

def reset_password(request):
    email = request.session.get('reset_email')  # Assuming email stored in session
    if not email:
        messages.error(request, 'Eiyo: Did you input your email?')
        return redirect('user:forgot_password')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # correct_otp = request.session.get('reset_otp') # Assumption
        correct_otp = OtpToken.objects(user=email).first()

        # Validate OTP
        if otp != correct_otp.otp_code:
            messages.error(request, 'Incorrect OTP!')
            return redirect('user:reset_password')
        
        # Check outdate OTP
        if datetime.now() > correct_otp.expires_at:
            messages.error(request, 'Outdated OTP!')
            return redirect('user:forgot_password')

        # Validate password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('user:reset_password')

        # Update password logic
        
        user = User.objects(email=email).first()
        if user:
            del request.session['reset_email']
            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password reset successfully! Please sign in.')
            return redirect('user:signin')

    return render(request, 'components/reset_password.html')
