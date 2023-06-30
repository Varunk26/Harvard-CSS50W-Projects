from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required



from .models import User, Listing, Bids


def index(request):
    return render(request, "auctions/index.html", {
        "activelisting": Listing.objects.all()
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
            # user.user_id = userid
            # user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def createlisting(request):

    if request.method == "POST":

        # accessing & storing itemname, description & url
        new_listing = Listing()
        new_listing.title = request.POST["title"]
        new_listing.description = request.POST["description"]

        # new_listing.bid =request.POST["startingbid"]
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        new_listing.createdby = user

        if request.POST["urllink"] is not None:
            new_listing.urllink = request.POST.get("urllink", "")

        new_listing.save()

        # accessing and storing bid, bid listing, bid by user and bid status
        new_bid = Bids()
        new_bid.bid = request.POST["startingbid"]
        new_bid.starting_bid = request.POST["startingbid"]
        new_bid.biduser = user.id
        new_bid.status = True

        #connect new bid foreign key to id of listing
        new_bid.bid_listing = new_listing
        new_bid.save()
                  
        
        # reverse not working
        return HttpResponseRedirect(reverse("auctions:index"))

    else:
        return render(request, "auctions/createlisting.html")

@login_required(login_url='login')
def listingpage(request, listing_id):        

    # get listing details
    current_listing = Listing.objects.get(id=listing_id)
    user_id = request.user.id

    #get bidding details. pk will be same as listing id
    listing_bid = Bids.objects.get(bid_listing=current_listing)

    # check if assosciated user id matchs with listing id
    
    watchlist_exists = current_listing.users.filter(id=user_id).exists()

    #check if logged in user is the creator of the listing

    if user_id is current_listing.createdby.id:
        iscreator = True
    else:
        iscreator = False

 
    return render(request, "auctions/listingpage.html", {
        "listing": current_listing,
        'user_id': user_id,
        "watchlist_exists": watchlist_exists,
        "bid": listing_bid,
        "iscreator": iscreator
    })

@login_required(login_url='login')
def addwatchlist(request, listing_id):

    if request.method == "POST":

        # accessing the listing
        listing = Listing.objects.get(pk=listing_id)

        # accessing the user
        # user_id = int(request.GET.get('arg1'))

        user_id = int(request.POST.get('user_id'))

        # finding the user assosciated with id

        user = User.objects.get(pk=user_id)

        # adding listing to user
        user.listings.add(listing)

        # Redirect User
        return HttpResponse("added to watch list wit user_ id" + str(user_id))

    else:
        return HttpResponse("not added")

@login_required(login_url='login')
def removewatchlist(request, listing_id):

    if request.method == "POST":

        # accessing the listing
        listing = Listing.objects.get(pk=listing_id)

        # accessing the user
        # user_id = int(request.GET.get('arg1'))

        user_id = int(request.POST.get('user_id'))

        # finding the user assosciated with id
        user = User.objects.get(pk=user_id)

        # remove listing from user
        user.listings.remove(listing)

        # Redirect User
        return HttpResponse("removed listing from watch list")

    else:
        return HttpResponse("failed to remove")    


@login_required(login_url='login')
def placebid(request, listing_id):

     # Update the existing bid assosciated with the listing

    if request.method == "POST":

        # accessing the listing
        listing = Listing.objects.get(pk=listing_id)

        #accessing the bid (bid id is the same as the listing id as they are created together)
        bid = Bids.objects.get(pk=listing_id)

        # accessing the user id that submitted the bid
        user_id = int(request.POST.get('user_id'))

        # accessing the bid
        placed_bid = int(request.POST.get('bid'))

        #Updating bid
        #check if bid is higher than current bid, status if false
        if bid.bid >= placed_bid or bid.starting_bid > placed_bid:
            return HttpResponse("Placed bid must be greater than existing bid")
        else:
            bid.bid = placed_bid
            bid.biduser = user_id

            bid.save()

        return HttpResponseRedirect(reverse("auctions:index"))

    else:
        HttpResponse("Bid adding error")

@login_required(login_url='login')
def closeauction(request, listing_id):

    if request.method == "POST":

        # access listing
        current_listing = Listing.objects.get(id=listing_id)

        # access bid
        listing_bid = Bids.objects.get(bid_listing=current_listing)

        # change bid status
        listing_bid.status = False
        listing_bid.save

        #return HttpResponse("auction closed and bid status is now" + str(listing_bid.status))

        return HttpResponseRedirect(reverse("auctions:index"))

    
        






