from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *


# finish signup and login functionality than make seller and customer dashboards
# after that make product model and views
# add some products via suppliers dashboard
# add basic profile changin etc functionality for customer
# make order model and views
#       we can use the order model to track order give updates and tranfer related files allowing access only where it is required
# add basic order functionality for customer
# add basic order functionality for supplier



def loginView(request):
    if request.user.is_authenticated:
        try:
            return redirect(f'{request.session.get("userType",None)}Dashboard')
        except:
            pass
    return render(request, 'login.html')



# modify these views to fit requirements 
# login will redirect based upon the user type

# save userType in request session and redirect to dashboard which will render based upon the userType
# figure out o=how to direct to respective dashboard i dont want brute forcing actually come up with a clever solution
# simply use the userType to redirect to respective dashboard and on each dashboard check if the user is authenticated and if the userType is correct
# if not redirect to login page with message saying no {userType} of name {username} found 
def loginUser(request):
    if request.user.is_authenticated: 
        logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userType = request.POST.get('userType')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print(userType)
            request.session['userType'] = userType
            # try
            return redirect(f'{userType}Dashboard')
            # except:
                # messages.info(request, f'No {userType} dashboard found')
                # return redirect('loginView')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html')

def signupUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cnfrmPassword = request.POST.get('cnfrmPassword')
        if password != cnfrmPassword:
            messages.error(request, 'Passwords do not match')
            return redirect('loginView')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('loginView')
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        customer = Customer.objects.create(user=user, name=username)
        customer.save()
        messages.info(request, 'Signup successful! Please login to continue.')
        return redirect('loginView')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    request.session['userType'] = None
    return redirect('loginView')

