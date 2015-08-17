from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from osp.models import Item, Basket, Customer
from django.core.urlresolvers import reverse
from django.db import IntegrityError

def index(request):
    item_list = Item.objects.all()
    context = {'item_list': item_list}
    return render(request, 'osp/index.html', context)

def basket(request, basket):
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

    t = item.purchase_quantity * item.cost
    
    try:
        basket = Basket(customer=c, totalbill=t)
        basket.save()
    except IntegrityError:
        basket = Basket.objects.get(customer=c)
        basket.totalbill += t

    basket.item_set.add(item)    
    return HttpResponseRedirect(reverse('osp:basket', args=(basket,)))
