from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<prod_name>[A-z]+[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<prod_name>[A-z]+[0-9]+)/basket/$', views.add_to_basket, name='add_to_basket'),
    url(r'^(\w+\d+)/basket/(?P<basket>[A-z]+)/$', views.basket, name='basket'),
    #url(r'^basket/(?P<basket>basket)/$', views.basket, name='basket'),
]
