from django.conf.urls import patterns, url

urlpatterns = patterns(
    'KyubeyUser.views',

#    url(r'^$','index'),
    
    url(r'^json/$','json'),
    url(r'^cmd.js$','cmd_js'),

)
