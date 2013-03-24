from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MomohaFeed.forms import SubscriptionAddForm
from MomohaFeed.models import Feed, Subscription
from django.core.exceptions import PermissionDenied
from MomohaFeed import poll

# Create your views here.

@login_required
def list_subscription(request):
    db_subscription_list = Subscription.objects.filter(
        user__exact = request.user
    ).select_related("feed")
    return render(request,"MomohaFeed/list_subscription.tmpl",{"subscription_list":db_subscription_list})

@login_required
def subscription_add(request):
    form = None
    if request.method == "POST":
        form = SubscriptionAddForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            db_feed = None
            db_subscription = None
            try:
                db_feed = Feed.objects.get(
                    url__exact = url
                )
            except Feed.DoesNotExist:
                db_feed = Feed.objects.create(
                    url = url
                )
            try:
                db_subscription = Subscription.objects.get(
                    user__exact = request.user,
                    feed__exact = db_feed,
                    end = None
                )
            except Subscription.DoesNotExist:
                db_subscription = Subscription.objects.create(
                    user = request.user,
                    feed = db_feed
                )
            
            poll(db_feed.id)
            
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
    return redirect("MomohaFeed.views.subscription_list_content",subscription_id=db_subscription.id)

@login_required
def subscription_list_content(request,subscription_id):
    # TODO
    return render(request,"dummy.tmpl")

@login_required
def subscription_content_show(request,subscriptioncontent_id):
    # TODO
    return render(request,"dummy.tmpl")

@login_required
def subscription_content_mark_read(request,subscriptioncontent_id):
    # TODO
    return render(request,"dummy.tmpl")
