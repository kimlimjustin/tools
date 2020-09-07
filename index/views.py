from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from index.models import User
from django.core.files.storage import FileSystemStorage
# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "index/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
    	if request.user.is_authenticated:
    		return HttpResponseRedirect(reverse('index'))
    	return render(request, "index/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "index/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "index/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
    	if request.user.is_authenticated:
    		return HttpResponseRedirect(reverse('index'))
    	return render(request, "index/register.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def index(request):
	return render(request, "index/index.html")
