from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from osp.models import Item, Basket, Customer, Transaction, Wishlist
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import datetime
from django.contrib.auth.decorators import login_required


def userassert(req):
    if req.user.is_authenticated():
        return req.user.username
    else:
        return 'defaultguest'

def index(request):
    item_list = Item.objects.all()
    context = {'item_list': item_list}
    return render(request, 'osp/index.html',context)


def basket(request):
    current_user = userassert(request)
    try:
        basket = Basket.objects.get(current=True, customer__name=current_user)
    except ObjectDoesNotExist:
        try:
            c = Customer.objects.get(name=current_user)
        except ObjectDoesNotExist:
            c = Customer(name=current_user)
            c.save()
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
    current_user = userassert(request)
    item = Item.objects.get(name=prod_name)
    try:
        c = Customer.objects.get(name=current_user)
    except ObjectDoesNotExist:
        c = Customer(name=current_user)
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


def add_to_wishlist(request, prod_name):
    current_user = userassert(request)
    item = Item.objects.get(name=prod_name)
    try:
        c = Customer.objects.get(name=current_user)
    except:
        c = Customer(name=current_user)
        c.save()

    try:
        wishlist = Wishlist.objects.get(customer__name=current_user)
    except ObjectDoesNotExist:
        wishlist = Wishlist(customer=c)
        wishlist.save()
    wishlist.item_set.add(item)
    return HttpResponseRedirect(reverse('osp:wishlist'))


def wishlist(request):
    current_user = userassert(request)
    try:
        wishlist = Wishlist.objects.get(customer__name=current_user)
    except ObjectDoesNotExist:
        try:
            c = Customer.objects.get(name=current_user)
        except ObjectDoesNotExist:
            c = Customer(name=current_user)
            c.save()
        wishlist = Wishlist(customer=c)
        wishlist.save()
    context = {'wishlist': wishlist}
    return render(request, 'osp/wishlist.html', context)


def checkout(request):
    current_user = userassert(request)
    basket = Basket.objects.get(current=True)
    c = Customer.objects.get(name=current_user)
    
    try:
        transaction = Transaction(date=datetime.now(), customer=c)
        transaction.save()
    except IntegrityError:
        transaction = Transaction.objects.get(customer__name=current_user)
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
    current_user = userassert(request)
    try:
        transaction = Transaction.objects.get(customer__name=current_user)
    except ObjectDoesNotExist:
        # Create dummy Transaction object
        c = Customer(name='dummy')
        c.save()
        transaction = Transaction(date=None, customer=c)  
        pass
    return render(request, 'osp/history.html', {'t': transaction})


def add_item(request):
    current_user = userassert(request)
    if request.method == 'POST':
        n = request.POST['itemname']
        c = int(request.POST['cost'])
        d = int(request.POST['discount'])
        a = int(request.POST['available'])
        newitem = Item(name=n, cost=c, discount=d, available=a, seller=current_user)
        newitem.save()
        return render(request, 'osp/itemadded.html',) 
    else:
        return render(request, 'osp/additem.html',)
