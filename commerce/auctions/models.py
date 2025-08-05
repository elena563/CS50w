from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


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

class Bid(models.Model):
    price = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()