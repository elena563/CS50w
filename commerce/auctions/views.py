from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import NewListingForm

from .models import User, Listing, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required
def create(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)

            if Listing.objects.filter(name=listing.name).exists():
                return render(request, "auctions/create.html", {
                    'form': form,
                    "error": "Listing already exists"
                })
            listing.owner = request.user
            
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[listing.name]))
        else:
            return render(request, "auctions/create.html", {
                    'form': NewListingForm(),
                    "error": "Invalid data"
                })
    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })


def listing(request, name): 
    listing = Listing.objects.filter(name=name).first()
    highest_bid = listing.bids.order_by('-price').first()

    if listing is not None:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "highest_bid": highest_bid
        })
    else:
        return render(request, "auctions/index.html", {
            "error": "Listing has been deleted or removed"
        })
    
@login_required
def comment(request, name):
    if request.method == 'POST':
        listing = Listing.objects.get(name=name)
        comment_text = request.POST.get("comment")
        Comment.objects.create(
            listing=listing,
            author=request.user,
            text=comment_text
        )
        return HttpResponseRedirect(reverse('listing', args=[listing.name]))
    
@login_required
def bid(request, name):
    if request.method == 'POST':
        listing = Listing.objects.get(name=name)
        highest_bid = listing.bids.order_by('-price').first().price if listing.bids.exists() else 0
        price = float(request.POST.get("price"))
        if (price <= listing.price) or (price < highest_bid):
            return render(request, "auctions/listing.html", {
                "listing": listing,
            "error": "Bid has to be as large as the starting price and higher than the highest bid"
        })
        Bid.objects.create(
            listing=listing,
            bidder=request.user,
            price=price
        )
        return HttpResponseRedirect(reverse('listing', args=[listing.name]))

def cancel(request, name):
    if request.method == "POST":
        listing = Listing.objects.get(name=name)
        if request.user == listing.owner:
            listing.is_active = False
            listing.save()
    return HttpResponseRedirect(reverse('listing', args=[listing.name]))
