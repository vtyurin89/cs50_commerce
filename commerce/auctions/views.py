from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment
from .forms import CreateListingForm, BidAmountForm
from .utils import check_cyrillic, translate_cyrillic, create_unique_slug

"""
TODO
 - Add positive price validator
 - Bids price - floatfield
 - No null comments
 - Make category optional
"""



def index(request):
    categories = Category.objects.all()
    active_listings = Listing.objects.filter(is_active=True).order_by("-id")

    #pagination
    pagination_range = 12
    paginator = Paginator(active_listings, pagination_range)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'context_menu_pos': 1,
        'categories': categories,
        'listings': active_listings,
        'page_obj': page_obj,
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
    form = CreateListingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.creator = request.user
            find_cyrillic = check_cyrillic(new_listing.title)
            if find_cyrillic:
                translated_title = translate_cyrillic(new_listing.title)
                new_listing.slug = create_unique_slug(translated_title)
            else:
                new_listing.slug = create_unique_slug(new_listing.title)
            new_listing.save()
            return redirect('index')
    context = {
        'context_menu_pos': 4,
        'form': form,
    }
    return render(request, "auctions/create_listing.html", context)


def categories(request):
    categories = Category.objects.all()
    context = {
        'context_menu_pos': 2,
        'categories': categories,
    }
    return render(request, "auctions/categories.html", context)


@login_required
def watchlist(request):
    context = {
        'context_menu_pos': 3,
    }
    return render(request, "auctions/watchlist.html", context)


def show_category(request, cat_slug):
    category = Category.objects.get(slug=cat_slug)
    cat_listings = Listing.objects.filter(cat=category).order_by("-id")

    #pagination
    pagination_range = 12
    paginator = Paginator(cat_listings, pagination_range)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'context_menu_pos': 2,
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, "auctions/show_category.html", context)


def show_listing(request, listing_slug):
    try:
        listing = Listing.objects.get(slug=listing_slug)
    except ObjectDoesNotExist:
        raise Http404
    bid_form = BidAmountForm(request.POST or None)

    if request.method=='POST':
        if 'bid_amount' in request.POST:
            bid_form = BidAmountForm(request.POST, listing=listing)
            if bid_form.is_valid():
                new_bid = bid_form.save(commit=False)
                new_bid.bidder = request.user
                new_bid.listing = listing
                new_bid.save()
                return redirect('show_listing', listing_slug=listing_slug)

        elif 'comment' in request.POST and request.POST['comment'] != '':
            new_comment = Comment.objects.create(
                comment_text=request.POST['comment'],
                comment_author=request.user,
                listing=listing,
            )
            return redirect('show_listing', listing_slug=listing_slug)
    bids = Bid.objects.filter(listing=listing).order_by("-bid_amount")
    max_bid = None
    if bids:
        max_bid = bids[0]
    comments = Comment.objects.filter(listing=listing, is_active=True).order_by("-id")
    context = {
        'context_menu_pos': 1,
        'listing': listing,
        'bids': bids,
        'max_bid': max_bid,
        'comments': comments,
        'bid_form': bid_form,
    }
    return render(request, "auctions/show_listing.html", context)
