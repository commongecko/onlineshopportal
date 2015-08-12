from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shop_portal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('osp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
