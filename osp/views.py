from django.shortcuts import render
from django.http import HttpResponse
from osp.models import Item

def index(request):
    item_list = Item.objects.all()
    return HttpResponse(item_list)
