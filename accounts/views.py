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
    full_name = user.person.full_name
    phone = user.person.number
    inventory_data = user.person.inventory_for_assigned_location()
    location = user.person.get_assigned_location_name()
    statments = user.person.get_statement()
    context = {
        "name": full_name,
        "phone": phone,
        "location": location,
        "inventory": inventory_data,
        "statements": statments,
    }
    return render(request, "accounts/userInfo.html", context)


def userInfoOwn(request, userId): 
    pass

def addEach(lstOpt, persons):
    for each in persons:
        lstOpt.append((each.id, each))
    return lstOpt


@login_required(login_url="login")
@user_assigned_location
def locationInfo(request, location_id):
    location = Location.objects.get(id=location_id)
    inventory_data = location.get_inevn_data()
    statments = location.get_statement()
    unassigned_persons = Person.objects.filter(location__isnull = True)
    options = []
    if location.person:
        options.append((location.person.id, location.person))
        options = addEach(options, unassigned_persons)
        options.append((-1, 'None'))
    else:
        options.append((-1, 'None'))
        options = addEach(options, unassigned_persons)
    
    context = {'location': location,
               'inventory': inventory_data,
               'statements': statments,
               'unassigned': options,
               'size': len(options)}
    
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


def update_assigned(request):
    if request.method == 'POST':
        if request.user.person.is_owner:
            selected_person = request.POST.get('selected_person')
            location_id = request.POST.get('location_id')

            try:
                loc = Location.objects.get(id=location_id)
                per = None
                print(type(selected_person))
                if selected_person != '-1':
                    per = Person.objects.get(id=selected_person)
                loc.person = per
                loc.save()
                messages.success(request, 'Location assigned updated successfully.')
            except:

                messages.error(request, 'Invalid Try Again')
        else:
            messages.error(request, 'Permission denied. You are not allowed to make changes.')
    return redirect('locationInfo', location_id=location_id)

def update_location(request):
    if request.method == 'POST':
        if request.user.person.is_owner:
            new_location_name = request.POST.get('new_location_name')
            location_id = request.POST.get('location_id')
            
            try:
                loc = Location.objects.get(id=location_id)
                loc.name = new_location_name
                loc.save()
                messages.success(request, 'Location name updated successfully.')
            except:
                messages.error(request, 'Invalid Try Again')
        else:
            messages.error(request, 'Permission denied. You are not allowed to make changes.')
    return redirect('locationInfo', location_id=location_id)


def update_FullName(request):
    if request.method == 'POST':
        per_id = request.POST.get('user_id')
        if request.user.person.is_owner or request.user.person.id == per_id:
            try:
                per = Person.objects.get(id=per_id)
                new_name = request.POST.get('new_Name')
                per.full_name = new_name
                per.save()
                messages.success(request, 'Full Name updated successfully.')
            except:
                messages.error(request, 'Invalid Try Again')
        else:
            messages.error(request, 'Permission denied. You are not allowed to make changes.')       
    return redirect('userInfo')