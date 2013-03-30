from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MomohaFeed.forms import SubscriptionAddForm
from MomohaFeed.models import Feed, Subscription, Item, ItemRead
from django.core.exceptions import PermissionDenied
from MomohaFeed import poll

# Create your views here.

@login_required
def list_subscription(request):
    db_subscription_list = Subscription.objects.filter(
        user__exact = request.user
    ).select_related("feed")

    return render(request,"MomohaFeed/list_subscription.tmpl",{
        "db_subscription_list":db_subscription_list,
        "add_form":SubscriptionAddForm()
    })

@login_required
def subscription_add(request):
    form = None
    if request.method == "POST":
        form = SubscriptionAddForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            db_feed,_ = Feed.objects.get_or_create(
                url = url
            )
            db_subscription,_ = Subscription.objects.get_or_create(
                user = request.user,
                feed = db_feed,
                enable = True
            )
            poll(db_feed)
            return redirect("MomohaFeed.views.subscription_list_content",subscription_id=db_subscription.id)
    if form == None:
        form = SubscriptionAddForm()
    return render(request,"MomohaFeed/subscription_add.tmpl",{"form" : form})

@login_required
def subscription_rm(request,subscription_id):
    # TODO
    return render(request,"dummy.tmpl")

@login_required
def subscription_poll(request,subscription_id):
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    poll(db_subscription.feed)
    return redirect("MomohaFeed.views.subscription_list_content",subscription_id=db_subscription.id)

@login_required
def subscription_list_content(request,subscription_id):
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    # db_item_list = Item.objects.filter(feed=db_subscription.feed)
    db_item_list = Item.objects.raw(
        '''
            SELECT * FROM MomohaFeed_item
            WHERE
                feed_id = %s AND
                NOT EXISTS (
                    SELECT * FROM MomohaFeed_itemread
                    WHERE
                        subscription_id = %s AND
                        item_id = MomohaFeed_item.id AND
                        enable
                )
            ORDER BY published DESC
        ''',
        [
            db_subscription.feed.id , db_subscription.feed.id
        ]
    )

    return render(request,"MomohaFeed/subscription_list_content.tmpl",{
        "db_subscription" : db_subscription,
        "db_item_list" : db_item_list
    })

@login_required
def subscription_item_show(request,subscription_id,item_id):
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    db_item = Item.objects.get(id=item_id)
    
    ItemRead.objects.get_or_create(
        subscription = db_subscription,
        item = db_item,
        enable = True
    )
    
    return render(request,"MomohaFeed/subscription_item_show.tmpl",{
        "db_subscription" : db_subscription,
        "db_item" : db_item
    })

@login_required
def subscription_item_mark_read(request,subscription_id,item_id):
    # TODO
    return render(request,"dummy.tmpl")
