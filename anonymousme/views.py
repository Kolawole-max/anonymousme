from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from time import gmtime, strftime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def landingpage(request):
    return render(request, 'anonymous/landingpage.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index", user_username=request.user.username)
        else:
            try:
                User.objects.get(username=username)
                return render(request, "anonymous/login.html", {
                    "message": 'Incorrect password'
                })
            except User.DoesNotExist:
                return render(request, "anonymous/login.html", {
                    "message": 'Invalid Username. Make sure you input the correct username'
                })
    else:
        return render(request, "anonymous/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["name"]
        password = request.POST["password"]

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "anonymous/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index", user_username=request.user)
    else:
        return render(request, "anonymous/register.html")


def profile(request, user_username):
    try:
        User.objects.get(username=user_username)

        if request.user.username == user_username:
            return render(request, 'anonymous/profile.html', {
                'profile' : user_username
            })
        else:
            return render(request, 'anonymous/reply.html', {
                'profile' : user_username
            })
    except User.DoesNotExist: 
        return render(request, 'anonymous/reply.html', {
            'none' : user_username
        })


def send(request, username):
    if request.method == "POST":
        
        content = request.POST["content"]
        try:
            user = User.objects.get(username=username)
            message_obj = Message.objects.create(
                message = content
            )
            user.message.add(message_obj)
            
            try:
                User.objects.get(username=request.user.username)
                return redirect("index", user_username=request.user.username)
            except User.DoesNotExist:
                return render(request, "anonymous/register.html", {
                "message": "Now it's your turn to create an account and dare your friends to tell you what they think about you!"
            })

        except User.DoesNotExist:
            return render(request, 'anonymous/reply.html', {
            'none' : username
        })
    else:
        return render(request, "anonymous/register.html")

# Fetch API
def load(request, username):
    try:
        
        if request.user.username == username:
            messages = User.objects.filter(username=username)
            return JsonResponse([message.serialize() for message in messages], safe=False)
        else: 
            return JsonResponse({"error": "Not your profile. Thief."}, status=404)
    except User.DoesNotExist:
        return HttpResponse(f'Error Page... 419 :)')
    