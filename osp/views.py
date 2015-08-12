from django.shortcuts import render
from django.http import HttpResponse
from osp.models import Item

def index(request):
    item_list = Item.objects.all()
    context = {'item_list': item_list}
    return render(request, 'osp/index.html', context)

def basket(request):
    pass

def detail(request, prod_name):
    item = Item.objects.get(name=prod_name)
    context = {'item': item}
    return render(request, 'osp/detail.html', context)
