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
        if req.user.username == 'admin':
            return 'defaultguest'
        else:
            return req.user.username
    else:
        return 'defaultguest'


def index(request):
    if request.user.has_perm('osp.change_item'):
        item_list = Item.objects.filter(listed=True, seller=request.user.username)
    else:
        item_list = Item.objects.filter(listed=True)
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
    context = {'basket': basket}
    return render(request, 'osp/basket.html', context)


def detail(request, prod_name):
    item = Item.objects.get(name=prod_name, listed=True)
    if request.user.has_perm('osp.change_item') and item.seller == request.user.username:
        edit = True
    else:
        edit = False

    context = {'item': item,
               'edit': edit }
    return render(request, 'osp/detail.html', context)


def add_to_basket(request, prod_name):
    current_user = userassert(request)

    try:
        c = Customer.objects.get(name=current_user)
    except ObjectDoesNotExist:
        c = Customer(name=current_user)
        c.save()

    try:
        basket = Basket.objects.get(current=True, customer=c)
    except ObjectDoesNotExist:
        basket = Basket(customer=c, totalbill=0, current=True)
        basket.save()

    try:
        item = basket.item_set.get(name=prod_name)
    except ObjectDoesNotExist:
        item = Item.objects.get(name=prod_name, listed=True)
        # Create an unlisted copy of item
        item.pk = None
        item.id = None
        item.wishlist_id = None
        item.listed = False
        item.save()
        basket.item_set.add(item)    

    item.purchase_quantity += int(request.POST['numofitems'])
    dis = (item.discount/100) * item.cost
    t = (item.purchase_quantity * item.cost) - dis
    item.save()
    basket.totalbill += t
    basket.save()

    return HttpResponseRedirect(reverse('osp:basket'))


def add_to_wishlist(request, prod_name):
    current_user = userassert(request)
    item = Item.objects.get(name=prod_name, listed=True)
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
    basket = Basket.objects.get(current=True, customer__name=current_user)
    c = Customer.objects.get(name=current_user)
    
    try:
        transaction = Transaction(customer=c)
        transaction.save()
    except IntegrityError:
        transaction = Transaction.objects.get(customer__name=current_user)
        transaction.basket_set.add(basket)
    
    try:
        basket = Basket.objects.get(current=True, customer=c)
        basket.date = datetime.now()
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
        transaction = Transaction(customer=None)  
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


def edit_item(request, prod_name):
    item = Item.objects.get(name=prod_name, listed=True)
    if request.user.has_perm('osp.change_item') and item.seller == request.user.username:
        edit = True
    else:
        edit = False

    context = {'item': item,
               'edit': edit }

    if request.method == 'POST':
        item.name = request.POST['itemname']
        item.cost = int(request.POST['cost'])
        item.discount = int(request.POST['discount'])
        item.available = int(request.POST['available'])
        item.save()
        return HttpResponseRedirect(reverse( 'osp:detail', args=(item.name,)))
    else:
        return render(request, 'osp/edititem.html', context)


def del_item(request, prod_name):
    item = Item.objects.get(name=prod_name, listed=True)
    if request.user.has_perm('osp.delete_item') and item.seller == request.user.username:
        item.delete()

    return HttpResponseRedirect(reverse('osp:index'))


def item_history(request, prod_name):
    seller_item_basket = Basket.objects.filter(item__name=prod_name)
    return render(request, 'osp/itemhistory.html', 
                  {'seller_item_basket': seller_item_basket,
                   'item'              : prod_name })


def logged_out(request):
    """
    Custom view to render logged out template 
    as the default logout view would not render it

    """
    return render(request, 'osp/logged_out.html',)

