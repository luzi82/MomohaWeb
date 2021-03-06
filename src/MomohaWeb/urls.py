from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import django.views.static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$',RedirectView.as_view(url='feed/'), name='index'),
    # url(r'^MomohaWeb/', include('MomohaWeb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^dj/admin/', include(admin.site.urls)),
#    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^api/feed/', include('MomohaFeed.urls')),
    url(r'^api/auth/', include('KyubeyAuth.urls')),
#    url(r'^/feed/$', RedirectView.as_view(url='feed/index.html') ),
)
