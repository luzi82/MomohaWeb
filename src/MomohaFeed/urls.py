from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns(
    'MomohaFeed.views',
    url(r'^$',RedirectView.as_view(url='s/')),
    url(r'^s/$','listSubscription'),
    url(r'^s\.add/$','subscriptionAdd'),
    url(r'^s/(?P<subscription_id>\d+)/rm/$','subscriptionRm'),
    url(r'^s/(?P<subscription_id>\d+)/$','subscriptionListContent'),
    url(r'^sc/(?P<subscriptioncontent_id>\d+)/$','subscriptionContentShow'),
    url(r'^sc/(?P<subscriptioncontent_id>\d+)/read/$','subscriptionContentMarkRead'),
)
