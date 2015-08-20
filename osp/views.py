from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from osp.models import Item, Basket, Customer, Transaction
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import datetime


def index(request):
    item_list = Item.objects.all()
    context = {'item_list': item_list}
    return render(request, 'osp/index.html',context)


def basket(request):
    try:
        basket = Basket.objects.get(current=True)
    except ObjectDoesNotExist:
        c = Customer.objects.get(name='defaultguest')
        basket = Basket(customer=c, totalbill=0, current=True)
        basket.save()
        #dummyitem = Item('n', 0, 0, 0, 0, basket) 
    context = {'basket': basket}
    return render(request, 'osp/basket.html', context)


def detail(request, prod_name):
    item = Item.objects.get(name=prod_name)
    context = {'item': item}
    return render(request, 'osp/detail.html', context)


def add_to_basket(request, prod_name):
    #item = get_object_or_404(Item, pk=request.POST['item'])
    item = Item.objects.get(name=prod_name)
    try:
        c = Customer.objects.get(name='defaultguest')
    except:
        c = Customer(name='defaultguest')
        c.save()

    # TODO: Account for discount

    try:
        basket = Basket.objects.get(current=True)
    except ObjectDoesNotExist:
        item.purchase_quantity = int(request.POST['numofitems']) 
        t = item.purchase_quantity * item.cost
        item.save()
        basket = Basket(customer=c, totalbill=t, current=True)
        basket.save()
    else:
        item.purchase_quantity += int(request.POST['numofitems'])
        item.save()
        t = item.purchase_quantity * item.cost
        basket.totalbill += t
        basket.save()

    basket.item_set.add(item)    
    return HttpResponseRedirect(reverse('osp:basket'))


def checkout(request):
    basket = Basket.objects.get(current=True)
    c = Customer.objects.get(name='defaultguest')
    
    try:
        transaction = Transaction(date=datetime.now(), customer=c)
        transaction.save()
    except IntegrityError:
        transaction = Transaction.objects.get(customer__name='defaultguest')
        transaction.basket_set.add(basket)
    
    try:
        basket = Basket.objects.get(current=True)
        basket.current = False
        basket.save()
        transaction.basket_set.add(basket)
    except ObjectDoesNotExist:
        pass

    return render(request, 'osp/checkout.html', )


def history(request):
    transaction = Transaction.objects.get(customer__name='defaultguest')
    return render(request, 'osp/history.html', {'t': transaction})
