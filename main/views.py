from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import Sign_Up, CreateNewAccount

# Create your views here.
def registration(request):
    if request.method =='POST':
        form = Sign_Up(request.POST)
        if form.is_valid():
            form.save()
            # Log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('home')
    else:
        form = Sign_Up()
        return render(request, 'register.html', {'form':form}) 
        
    return render(request, 'register.html', {'form':form})
def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, try again...")
            return redirect('home')
    else:
        return render(request, "login.html", {})


def log_out(request):
    logout(request)
    messages.success(request, "You Have Logged Out...")
    return redirect('home')

def home(request):
    if request.method =="POST":
        form = CreateNewAccount(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            m = form.cleaned_data["account_type"]
            request.user.account_set.create(user = request.user, name=n, account_type=m)
        
        return HttpResponseRedirect("home")
    else:
        form = CreateNewAccount()

    return render(request, 'home.html', {'form':form})