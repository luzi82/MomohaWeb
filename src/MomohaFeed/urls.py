from django.conf.urls import patterns, url

urlpatterns = patterns(
    'MomohaFeed.views',
    url(r'^$','index'),
    url(r'^s/$','listSubscription'),
    url(r'^s.add/$','subscriptionAdd'),
    url(r'^s/(?P<subscription_id>\d+)/rm/$','subscriptionRm'),
    url(r'^s/(?P<subscription_id>\d+)/$','subscriptionListContent'),
    url(r'^sc/(?P<subscriptioncontent_id>\d+)/$','subscriptionContentShow'),
    url(r'^sc/(?P<subscriptioncontent_id>\d+)/read/$','subscriptionContentMarkRead'),
)
