from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')
        email = request.POST.get('email')
        user_exists = False
        try:
            User.objects.get(username=username)
            user_exists = True
        except:
            logger.debug('User does not exist')

        if not user_exists:
             user = User.objects.create_user(username=username, email=email, password=password)
             login(request, user)
             context['user'] = user
             return render(request,'main/index.html',context=context)
        else:
            context["error_message"] = "User already exists"
            return render(request,"users/register.html",context=context)

    return render(request,"users/register.html",context=context)