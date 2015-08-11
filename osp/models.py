from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=50)
    cost = models.IntegerField()
    discount = models.SmallIntegerField(default=0)
    available = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Basket(models.Model):
    totalbill = models.IntegerField()

class Transaction(models.Model):
    pass

class Customer(models.Model):
    basket = models.ForeignKey(Basket)
    history = models.ForeignKey(Transaction)
