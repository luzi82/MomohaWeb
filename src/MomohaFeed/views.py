from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MomohaFeed.forms import AddSubscriptionForm, post_form
from MomohaFeed.models import Subscription, Item
from django.core.exceptions import PermissionDenied
import MomohaFeed
from django.http import HttpResponse
import simplejson
from MomohaFeed.viewmodels import VmSubscription, VmItem, VmItemDetail

def json(f):
    def ff(request,*args,**kwargs):
        ret = f(request,*args,**kwargs)
        return HttpResponse(simplejson.dumps(ret), mimetype='application/json')
    return ff

def u403(f):
    def ff(request,*args,**kwargs):
        if request.user == None:
            raise PermissionDenied
        return f(request,*args,**kwargs)
    return ff

# Create your views here.

@login_required
def list_subscription(request):
    db_subscription_list = Subscription.objects.filter(
        user__exact = request.user
    ).select_related("feed")

    return render(request,"MomohaFeed/list_subscription.tmpl",{
        "db_subscription_list":db_subscription_list,
        "add_form":AddSubscriptionForm()
    })

@login_required
def subscription_add(request):
    form = None
    if request.method == "POST":
        form = AddSubscriptionForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            db_feed,db_subscription = MomohaFeed.subscription_add(request.user,url)
            MomohaFeed.feed_poll(db_feed)
            return redirect("MomohaFeed.views.subscription_list_content",subscription_id=db_subscription.id)
    if form == None:
        form = AddSubscriptionForm()
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
    MomohaFeed.feed_poll(db_subscription.feed)
    return redirect("MomohaFeed.views.subscription_list_content",subscription_id=db_subscription.id)

@login_required
def subscription_list_content(request,subscription_id):
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(db_subscription)

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

    MomohaFeed.subscription_item_mark_read(db_subscription, db_item)
    
    return render(request,"MomohaFeed/subscription_item_show.tmpl",{
        "db_subscription" : db_subscription,
        "db_item" : db_item
    })

@login_required
def subscription_item_mark_read(request,subscription_id,item_id):
    # TODO
    return render(request,"dummy.tmpl")

@u403
@json
def j_list_subscription(request):
    
    db_subscription_list = Subscription.objects.filter(
        user__exact = request.user,
        enable__exact = True
    ).select_related("feed")
    
    subscription_list = []
    for db_subscription in db_subscription_list:
        subscription_list.append(VmSubscription(db_subscription).__dict__)
    
    return {
        'subscription_list' : subscription_list
    }

@u403
@json
@post_form(AddSubscriptionForm)
def j_add_subscription(request,form):
    url = form.cleaned_data["url"]
    db_feed,db_subscription = MomohaFeed.subscription_add(request.user,url)
    MomohaFeed.feed_poll(db_feed)
    return {
        'success': True,
        'subscription' : VmSubscription(db_subscription).__dict__
    }

@u403
@json
@post_form(MomohaFeed.forms.SubscriptionSetEnableForm)
def j_subscription_set_enable(request,form):

    subscription_id = form.cleaned_data["subscription_id"]
    value = form.cleaned_data["value"]
    
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    db_subscription.enable = value
    db_subscription.save()
    
    return { 'success' : True }

@u403
@json
@post_form(MomohaFeed.forms.SubscriptionListItemForm)
def j_subscription_list_item(request,form):

    subscription_id = form.cleaned_data["subscription_id"]
    
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(db_subscription)
    
    item_list = []
    for db_item in db_item_list:
        item_list.append(VmItem(db_item).__dict__)

    return { 'item_list' : item_list }

@u403
@json
@post_form(MomohaFeed.forms.SubscriptionItemDetailForm)
def j_subscription_item_detail(request,form):
    
    subscription_id = form.cleaned_data["subscription_id"]
    item_id = form.cleaned_data["item_id"]
    
    # db_item = Item.objects.get(id=item_id)
    db_item = MomohaFeed.subscription_item_detail(subscription_id, item_id)
    
    return { 'item_detail': VmItemDetail(db_item).__dict__ }


@u403
@json
@post_form(MomohaFeed.forms.SubscriptionItemSetReaddoneForm)
def j_subscription_item_set_readdone(request,form):
    pass
