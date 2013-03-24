from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MomohaFeed.forms import SubscriptionAddForm
from MomohaFeed.models import Feed, Subscription

# Create your views here.

@login_required
def listSubscription(request):
    db_subscription_list = Subscription.objects.filter(
        user__exact = request.user
    ).select_related("feed")
    return render(request,"MomohaFeed/listSubscription.tmpl",{"subscription_list":db_subscription_list})

@login_required
def subscriptionAdd(request):
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
            return redirect("MomohaFeed.views.subscriptionListContent",subscription_id=db_subscription.id)
    if form == None:
        form = SubscriptionAddForm()
    return render(request,"MomohaFeed/subscriptionAdd.tmpl",{"form" : form})

@login_required
def subscriptionRm(request,subscription_id):
    # TODO
    return render(request,"dummy.tmpl")

@login_required
def subscriptionListContent(request,subscription_id):
    # TODO
    return render(request,"dummy.tmpl")

@login_required
def subscriptionContentShow(request,subscriptioncontent_id):
    # TODO
    return render(request,"dummy.tmpl")

@login_required
def subscriptionContentMarkRead(request,subscriptioncontent_id):
    # TODO
    return render(request,"dummy.tmpl")
