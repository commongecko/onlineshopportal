from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<prod_name>\w+\d+)/$', views.detail, name='detail'),
    url(r'^(?P<prod_name>\w+\d+)/basket/$', views.add_to_basket, name='add_to_basket'),
    url(r'^basket/$', views.basket, name='basket'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^history/$', views.history, name='history'),
]
