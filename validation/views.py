from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        fileInput = request.FILES.get('fileInput')  # Use request.FILES to get the uploaded file

        # Validate file size
        max_size_in_bytes = 2 * 1024 * 1024  # 2MB
        if fileInput and fileInput.size > max_size_in_bytes:
            return render(request, 'register.html', {'error': "Image file size exceeds 2MB."})

        # Hash the password
        hashed_password = make_password(password)

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=hashed_password,
            first_name=firstname,
            last_name=lastname,
        )

        # # Create a profile with the uploaded image
        # Profile.objects.create(
        #     user=user,
        #     profile_image=fileInput
        # )
        return redirect('login')
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,
        password=password
        )

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': "Invalid Username and Password"})
    else:
        return render(request, 'login.html')
        
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})