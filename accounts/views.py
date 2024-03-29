from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .form import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from .models import *
from http import HTTPStatus
from django.contrib.contenttypes.models import ContentType


# Create your views here.
@login_required(login_url="login")
@user_made_statement
def showST(request, STcode):
    ST = StoreStatement.objects.get(id=STcode)
    context = {"code": STcode, "statement": ST.get_ST_Info()}
    return render(request, "accounts/STinfo.html", context)


def getInfo(user):
    full_name = user.person.full_name
    phone = user.person.number
    inventory_data = user.person.inventory_for_assigned_location()
    location = user.person.get_assigned_location_name()
    statments = user.person.get_statement()
    restock = user.person.get_restock()

    context = {
        "id": user.person.id,
        "name": full_name,
        "phone": phone,
        "location": location,
        "inventory": inventory_data,
        "statements": statments,
        "restock": restock,
        "username": user.username,
    }
    return context


@login_required(login_url="login")
def userInfoEmp(request):
    user = User.objects.get(id=request.user.id)
    context = getInfo(user)
    return render(request, "accounts/userInfo.html", context)


@login_required(login_url="login")
@owner_required
def userInfoOwn(request, person_id):
    try:
        user = User.objects.get(person__id=person_id)
    except:
        return render(request, "accounts/my404.html", status=HTTPStatus.NOT_FOUND)
    context = getInfo(user)  # 7 kamesh
    # 8 darshana
    context["owner_view"] = True

    return render(request, "accounts/userInfoEmp.html", context)


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
    restock = location.get_restock()
    unassigned_persons = Person.objects.filter(location__isnull=True)
    stor = Store.objects.all()
    isAssigned = request.user.person.get_assigned_location_name() == location

    options = []
    if location.person:
        options.append((location.person.id, location.person))
        options = addEach(options, unassigned_persons)
        options.append((-1, "None"))
    else:
        options.append((-1, "None"))
        options = addEach(options, unassigned_persons)

    context = {
        "location": location,
        "inventory": inventory_data,
        "statements": statments,
        "unassigned": options,
        "restock": restock,
        "size": len(options),
        "isAssigned": isAssigned,
        "stores": stor,
    }

    return render(request, "accounts/locationInfo.html", context)


@login_required(login_url="login")
@owner_required
def registerPage(request):
    if request.method == "POST":
        if not request.user.person.is_owner:
            raise PermissionDenied("You are not allowed to make an user")
        username = request.POST.get("username")
        password1= request.POST.get("password1")
        password2= request.POST.get("password2")
        is_owner = request.POST.get("is_owner")
        if password1 != password2:
            messages.error(request, "Password does not match!!!")
            return render(request, "accounts/newReg.html", {"used": username})
        user = User.objects.create(username=username, password = password1)
        user.save()
        if is_owner:
            user.person.is_owner = True
            user.person.save()
        return redirect(reverse('userInfo', kwargs={'person_id': user.person.id}))
    context = {}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", None)
            if next_url:
                return redirect(next_url)
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
    if request.method == "POST":
        if request.user.person.is_owner:
            selected_person = request.POST.get("selected_person")
            location_id = request.POST.get("location_id")

            try:
                loc = Location.objects.get(id=location_id)
                per = None
                if selected_person != "-1":
                    per = Person.objects.get(id=selected_person)
                loc.person = per
                loc.save()
                messages.success(request, "Location assigned updated successfully.")
            except:
                messages.error(request, "Invalid Try Again")
        else:
            messages.error(
                request, "Permission denied. You are not allowed to make changes."
            )

        return redirect("locationInfo", location_id=location_id)
    return redirect("userInfo")


def update_location(request):
    if request.method == "POST":
        if request.user.person.is_owner:
            new_location_name = request.POST.get("new_location_name")
            location_id = request.POST.get("location_id")

            try:
                loc = Location.objects.get(id=location_id)
                loc.name = new_location_name
                loc.save()
                messages.success(request, "Location name updated successfully.")
            except:
                messages.error(request, "Invalid Try Again")
        else:
            messages.error(
                request, "Permission denied. You are not allowed to make changes."
            )
        return redirect("locationInfo", location_id=location_id)
    return redirect("userInfo")


def handle_user_update(request, new_entry_id, new_entry_type, user_id=None):
    if request.method == "POST":
        per_id = user_id if user_id is not None else request.user.person.id
        if request.user.person.is_owner or request.user.person.id == per_id:
            try:
                per = Person.objects.get(id=per_id)
                new_entry = request.POST.get(new_entry_id)
                nested_attributes = new_entry_type.split(".")
                cur = per
                for attr in nested_attributes[:-1]:
                    cur = getattr(cur, attr, None)

                setattr(cur, nested_attributes[-1], new_entry)
                cur.save()
                messages.success(request, "Full Name updated successfully.")
            except:
                messages.error(request, "Invalid Try Again")
        else:
            messages.error(
                request, "Permission denied. You are not allowed to make changes."
            )
    if user_id:
        return redirect("userInfo", user_id)
    return redirect("userInfo")


def update_FullName(request, user_id=None):
    return handle_user_update(request, "new_Name", "full_name", user_id)


def update_UserName(request, user_id=None):
    return handle_user_update(request, "new_UserName", "user.username", user_id)


def update_Number(request, user_id=None):
    return handle_user_update(request, "new_Number", "number", user_id)


def postStoreStatement(request):
    if request.method == "POST":
        itemList = Item.objects.all()
        location_id = request.POST.get("location_id")
        store_id = request.POST.get("store_select")
        try:
            store = Store.objects.get(id=store_id)
            loc = Location.objects.get(id=location_id)
        except:
            messages.error(request, "Didn't Find Store")
            return redirect("locationInfo", location_id=location_id)
        inven = loc.get_inevn_data
        stm = StoreStatement.objects.create(
            creator=request.user.person, warehouse=loc, customer=store
        )
        flag = False
        for each in itemList:
            num = int(request.POST.get("item-" + each.name))
            if num > loc.get_quntity_of_item(each):
                flag = True
                break
            elif num != 0:
                ItemQuantity.objects.create(
                    content_type=ContentType.objects.get_for_model(StoreStatement),
                    object_id=stm.id,
                    item=each,
                    quantity=num,
                )

        if flag:
            messages.error(request, "Not Enough Items")
            stm.delete()

    return redirect("locationInfo", location_id=location_id)


def postLocationStatement(self):
    pass
