from django.conf.urls import patterns, url

urlpatterns = patterns(
    'MomohaFeed.views',
    url(r'^$','list_subscription'),
    url(r'^s\.add/$','subscription_add'),
    url(r'^s/(?P<subscription_id>\d+)/rm/$','subscription_rm'),
    url(r'^s/(?P<subscription_id>\d+)/poll/$','subscription_poll'),
    url(r'^s/(?P<subscription_id>\d+)/$','subscription_list_content'),
    url(r'^s/(?P<subscription_id>\d+)/i/(?P<item_id>\d+)/$','subscription_item_show'),
    url(r'^s/(?P<subscription_id>\d+)/i/(?P<item_id>\d+)/read/$','subscription_item_mark_read'),
    
    url(r'^j_list_subscription/$','j_list_subscription'),
    url(r'^j_add_subscription/$','j_add_subscription'),
    url(r'^j_subscription_set_enable/(?P<subscription_id>\d+)/(?P<value>[01])/$','j_subscription_set_enable'),
    url(r'^j_subscription_list_item/(?P<subscription_id>\d+)/$','j_subscription_list_item'),
    url(r'^j_subscription_item_show/(?P<subscription_id>\d+)/(?P<item_id>\d+)/$','j_subscription_item_show'),
    url(r'^j_subscription_item_set_readdone/(?P<subscription_id>\d+)/(?P<item_id>\d+)/(?P<value>[01])/$','j_subscription_item_set_readdone'),
)
