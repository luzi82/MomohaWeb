from django.conf.urls import patterns, url

urlpatterns = patterns(
    'MomohaFeed.views',
    url(r'^$','list_subscription'),
    url(r'^s\.add/$','subscription_add'),
    url(r'^s/(?P<subscription_id>\d+)/rm/$','subscription_rm'),
    url(r'^s/(?P<subscription_id>\d+)/poll/$','subscription_poll'),
    url(r'^s/(?P<subscription_id>\d+)/$','subscription_list_content'),
    url(r'^sc/(?P<subscriptioncontent_id>\d+)/$','subscription_content_show'),
    url(r'^sc/(?P<subscriptioncontent_id>\d+)/read/$','subscription_content_mark_read'),
)
