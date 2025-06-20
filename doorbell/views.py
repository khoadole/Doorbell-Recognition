from django.shortcuts import render

def home(request):
    return render(request, 'homepage.html')

def get_popup_template(request):
    return render(request, 'components/popup.html')

def history(request):
    return render(request, 'components/history.html')

def profile(request):
    return render(request, 'components/profile.html')

def signin(request):
    return render(request, 'components/signin.html')

def signup(request):
    return render(request, 'components/signup.html')