from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from .models import *


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.person.is_owner:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('userInfo')

    return wrapper



def user_made_statement(view_func):
    def wrapper(request, STcode, *args, **kwargs):
        try:
            st = StoreStatement.objects.get(id=STcode)
        except StoreStatement.DoesNotExist:
            return render(request, 'accounts/my404.html')
        if st.creator == request.user.person or request.user.person.is_owner:
            return view_func(request, STcode, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to view this statement")
    return wrapper


def user_assigned_location(view_func):
    def wrapper(request, location_id, *args, **kwargs):
        try:
            lc = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return render(request, 'accounts/my404.html')
        if lc.person == request.user.person or request.user.person.is_owner:
            return view_func(request, location_id, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to view this statement")
    return wrapper



