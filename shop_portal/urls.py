from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shop_portal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('osp.urls', namespace="osp")),
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
)
