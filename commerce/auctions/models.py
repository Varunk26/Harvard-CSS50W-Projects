from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    pass

class Listing(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    urllink = models.URLField(blank=True)

    # remove bid
    # bid = models.IntegerField(max_digits=5) 
    # This user is for watchlist
    users = models.ManyToManyField(User, blank=True, related_name="listings")
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", default=0)

    pass

class Bids(models.Model):
    
    id = models.AutoField(primary_key = True)
    bid = models.IntegerField()
    starting_bid = models.IntegerField(default=0)
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    biduser = models.IntegerField()
    status = models.BooleanField(default=False)

    # pass

# class Comments(models.Model):
    # pass

# class Watchlist(models.Model):

    # watchlist_userid = models.ForeignKey(User, on_delete=models.CASCADE)
    # listing = models.ForeignKey(Listing, on_delete=models.CASCADE)