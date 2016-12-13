from django.shortcuts import render, redirect

from models import *

# Create your views here.
def index(request):
    return render(request, "loginapp/index.html");

def register(request):
    did_register = User.objects.register(request, request.POST)

    if did_register:
        return redirect("/dashboard")
    else:
        return redirect("/")

def login(request):
    did_login = User.objects.login(request, request.POST)

    if did_login:
        return redirect("/dashboard")
    else:
        return redirect("/")
