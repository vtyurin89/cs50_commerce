from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
    context = {
        'context_menu_pos': 1,
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    context = {
        'context_menu_pos': 1,
    }
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context["message"] = "Invalid username and/or password."
            return render(request, "auctions/login.html", context)
    else:
        return render(request, "auctions/login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    context = {
        'context_menu_pos': 1,
    }
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            context["message"] = "Passwords must match."
            return render(request, "auctions/register.html", context)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            context["message"] = "Username already taken."
            return render(request, "auctions/register.html", context)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", context)


@login_required
def create_listing(request):
    context = {
        'context_menu_pos': 4,
    }
    return render(request, "auctions/create_listing.html", context)


def categories(request):
    context = {
        'context_menu_pos': 2,
    }
    return render(request, "auctions/categories.html", context)


@login_required
def watchlist(request):
    context = {
        'context_menu_pos': 3,
    }
    return render(request, "auctions/watchlist.html", context)