from django.shortcuts import render, HttpResponse, redirect
from .form import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from .models import *


# Create your views here.
@login_required(login_url="login")
@user_made_statement
def showST(request, STcode):
    ST = StoreStatement.objects.get(id=STcode)
    context = {"code": STcode, "statement": ST.get_ST_Info()}
    return render(request, "accounts/STinfo.html", context)


@login_required(login_url="login")
def userInfoEmp(request):
    user = User.objects.get(id=request.user.id)
    f_name = user.person.first_name
    l_name = user.person.last_name
    phone = user.person.number
    inventory_data = user.person.inventory_for_assigned_location()
    location = user.person.get_assigned_location_name()
    statments = user.person.get_statement()
    print(inventory_data)
    context = {
        "name": f"{f_name} {l_name}",
        "phone": phone,
        "location": location,
        "inventory": inventory_data,
        "statements": statments,
    }
    return render(request, "accounts/userInfo.html", context)


def userInfoOwn(request, userId): 
    pass

@login_required(login_url="login")
@user_assigned_location
def locationInfo(request, location_id):
    location = Location.objects.get(id=location_id)
    inventory_data = location.get_inevn_data()
    statments = location.get_statement()
    context = {'location': location,
               'inventory': inventory_data,
               'statements': statments}
    return render(request, 'accounts/locationInfo.html', context)


@owner_required
def registerPage(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_owner = request.POST.get("is_owner") == "on"
            user.person.is_owner = is_owner
            user.person.save()
            return HttpResponse("Nice Cock")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.info(request, "Incorrect username or password")
    context = {}
    return render(request, "accounts/login.html", context)


@login_required(login_url="login")
@owner_required
def home(request):
    return render(request, "accounts/main.html")


def logoutUser(request):
    logout(request)
    return redirect("login")
