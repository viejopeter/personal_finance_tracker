from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render

def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context['user'] = user
            return render(request,'main/index.html',context=context)
        else:
            context['error_message'] = 'Invalid username or password'
            return render(request,'users/login.html',context=context)

    return render(request, 'users/login.html')

def logout_request(request):
    logout(request)
    return render(request,'main/index.html')

def register_request(request):
    context = {}

    return render(request,"users/register.html",context=context)