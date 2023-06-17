from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Name')
    slug = models.SlugField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=250, db_index=True, verbose_name='Title')
    slug = models.SlugField(max_length=270, db_index=True, unique=True)
    cat = models.ForeignKey('Category', verbose_name='Category', on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name='Description')
    starting_bid = models.FloatField(verbose_name='Starting bid')
    image = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='Is currently active')
    winner = models.ForeignKey('User', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Bid(models.Model):
    bidder = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
    bid_amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.bidder} bet {self.bid_amount}'


