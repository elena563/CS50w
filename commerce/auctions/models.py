from django.contrib.auth.models import AbstractUser
from django.db import models




class Listing(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    description = models.TextField()
    image = models.URLField(blank=True)

    CATEGORIES = [
        ('tech', 'Technology'),
        ('fash', 'Fashion'),
        ('ent', 'Entertainment'),
        ('sport', 'Sport'),
        ('toys', 'Toys'),
        ('home', 'Home'),
    ]

    category = models.CharField(max_length=30, choices=CATEGORIES)
    owner = models.CharField(max_length=64, null=True)
    is_active = models.BooleanField(default=True)

class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    wished = models.ManyToManyField(Listing, blank=True, related_name='wished_listings')


class Bid(models.Model):
    price = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()