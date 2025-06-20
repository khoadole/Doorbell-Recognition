from django.shortcuts import render, redirect

def home(request):
    return render(request, 'homepage.html')

def get_popup_template(request):
    return render(request, 'components/popup.html')

def history(request):
    return render(request, 'components/history.html')

def profile(request):
    username = request.session.get('username', 'Guest')  # fallback if not logged in
    return render(request, 'components/profile.html', {'username': username})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if password == "123":
            request.session['logged_in'] = True
            request.session['username'] = username  # 👈 lưu username
            return redirect('home')
        else:
            return render(request, 'components/signin.html', {'error': 'Incorrect password'})
    return render(request, 'components/signin.html')

def signup(request):
    return render(request, 'components/signup.html')

def signout(request):
    request.session.flush()
    return redirect('home')