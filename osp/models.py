from django.db import models
from datetime import datetime

class Customer(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    customer = models.OneToOneField(Customer, null=True)


class Basket(models.Model):
    customer = models.ForeignKey(Customer, null=True)
    totalbill = models.IntegerField()
    transaction = models.ForeignKey(Transaction, null=True)
    current = models.BooleanField(default=True)
    date = models.DateTimeField(default=datetime.now, blank=True)


class Wishlist(models.Model):
    customer = models.OneToOneField(Customer, null=True)


class Item(models.Model):
    name = models.CharField(max_length=50)
    cost = models.IntegerField()
    discount = models.SmallIntegerField(default=0)
    available = models.IntegerField(default=1)
    purchase_quantity = models.IntegerField(default=0)
    listed = models.BooleanField(default=True)
    basket = models.ManyToManyField(Basket)
    wishlist = models.ManyToManyField(Wishlist)
    seller = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.name

