from django.shortcuts import render

# Create your views here.

def base(request):
    
    return render(request, 'base.html')

def index(request):
    return render(request, 'Trackerfolder/index.html')


def auth_login(request):
    
    return render(request, 'Trackerfolder/auth-login.html')


def auth_reset_password(request):
    
    return render(request, 'Trackerfolder/auth-reset-password.html')