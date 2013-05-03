'''
@author: luzi82
'''

from django.contrib import admin
from MomohaFeed.models import Feed, Subscription

class FeedAdmin(admin.ModelAdmin):
    
    list_display = (
        'title',
        'url',
        'last_poll',
    )

admin.site.register(Feed, FeedAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    
    list_display = (
        'user',
        'feed_title',
    )
    list_filter = ['user']
    
admin.site.register(Subscription, SubscriptionAdmin)
