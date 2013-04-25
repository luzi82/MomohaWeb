from django.conf.urls import patterns, url

urlpatterns = patterns(
    'MomohaFeed.views',

#    url(r'^$','list_subscription'),
#    url(r'^s\.add/$','subscription_add'),
#    url(r'^s/(?P<subscription_id>\d+)/rm/$','subscription_rm'),
#    url(r'^s/(?P<subscription_id>\d+)/poll/$','subscription_poll'),
#    url(r'^s/(?P<subscription_id>\d+)/$','subscription_list_content'),
#    url(r'^s/(?P<subscription_id>\d+)/i/(?P<item_id>\d+)/$','subscription_item_show'),
#    url(r'^s/(?P<subscription_id>\d+)/i/(?P<item_id>\d+)/read/$','subscription_item_mark_read'),

#    url(r'^$','index'),
    
#    url(r'^j_list_subscription/$','j_list_subscription'),
#    url(r'^j_add_subscription/$','j_add_subscription'),
#    url(r'^j_subscription_set_enable/$','j_subscription_set_enable'),
#    url(r'^j_subscription_list_item/$','j_subscription_list_item'),
#    url(r'^j_subscription_list_item_detail/$','j_subscription_list_item_detail'),
#    url(r'^j_subscription_item_detail/$','j_subscription_item_detail'),
#    url(r'^j_subscription_item_set_readdone/$','j_subscription_item_set_readdone'),
#    url(r'^j_subscription_poll/$','j_subscription_poll'),

    url(r'^json/$','json'),
    url(r'^cmd.js$','cmd_js'),

)
