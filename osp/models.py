from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=50)
    cost = models.IntegerField()
    discount = models.SmallIntegerField(default=0)
    available = models.IntegerField(default=1)
    purchase_quantity = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

class Basket(models.Model):
    items = models.ManyToManyField(Item)
    totalbill = models.IntegerField()

class Transaction(models.Model):
    #datentime = models.DateTimeField('date of transaction')
    #order = models.ForeignKey(Basket)
    pass

class Customer(models.Model):
    name = models.CharField(max_length=50)
    basket = models.ForeignKey(Basket)
    history = models.ForeignKey(Transaction)

    def __unicode__(self):
        return self.name
