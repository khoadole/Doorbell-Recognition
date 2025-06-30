from django.shortcuts import render, redirect
from users.decorators import login_required

def home(request):
    return render(request, 'homepage.html')

def get_popup_template(request):
    return render(request, 'components/popup.html')

@login_required
def history(request):
    return render(request, 'components/history.html')
