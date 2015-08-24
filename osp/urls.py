from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<prod_name>.+)/basket/$', views.add_to_basket, name='add_to_basket'),
    url(r'^basket/$', views.basket, name='basket'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^history/$', views.history, name='history'),
    url(r'^wishlist/$', views.wishlist, name='wishlist'),
    url(r'^(?P<prod_name>.+)/wishlist/$', views.add_to_wishlist, name='add_to_wishlist'),
    url(r'^additem/$', views.add_item, name='add_item'),
    url(r'^edititem/(?P<prod_name>.+)/$', views.edit_item, name='edit_item'),
    url(r'^delitem/(?P<prod_name>.+)/$', views.del_item, name='del_item'),
    url(r'^itemhistory/(?P<prod_name>.+)/$', views.item_history, name='item_history'),
    url(r'^(?P<prod_name>.+)/details/$', views.detail, name='detail'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/logged_out/'}),
    url(r'^logged_out/$', views.logged_out, name='logged_out'),
]
