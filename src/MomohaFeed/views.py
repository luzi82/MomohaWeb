from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MomohaFeed.forms import SubscriptionAddForm
from MomohaFeed.models import Subscription, Item
from django.core.exceptions import PermissionDenied, ValidationError
import MomohaFeed
from django.http import HttpResponse
import simplejson

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
        "add_form":SubscriptionAddForm()
    })

@login_required
def subscription_add(request):
    form = None
    if request.method == "POST":
        form = SubscriptionAddForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            db_feed,db_subscription = MomohaFeed.subscription_add(request.user,url)
            MomohaFeed.feed_poll(db_feed)
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
        user__exact = request.user
    ).select_related("feed")
    
    subscription_list = []
    for db_subscription in db_subscription_list:
        subscription = {}
        subscription['title'] = db_subscription.feed.title
        subscription['id'] = db_subscription.id
        subscription_list.append(subscription)
    
    return {
        'subscription_list' : subscription_list
    }

@u403
@json
@MomohaFeed.forms.post_form(SubscriptionAddForm)
def j_add_subscription(request,form):
    url = form.cleaned_data["url"]
    db_feed,db_subscription = MomohaFeed.subscription_add(request.user,url)
    MomohaFeed.feed_poll(db_feed)
    return {
        'success': True,
        'subscription_id' : db_subscription.id
    }

@u403
@json
def j_subscription_set_enable(request,subscription_id,value):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_subscription.enable = value != 0
    
    return { 'success' : True }

@u403
@json
@MomohaFeed.forms.post_form(MomohaFeed.forms.SubscriptionListItemForm)
def j_subscription_list_item(request,form):

    subscription_id = form.cleaned_data["subscription_id"]
    
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(db_subscription)
    
    item_list = []
    for db_item in db_item_list:
        item = {}
        item['title'] = db_item.title
        item['published'] = db_item.published
        item['id'] = db_item.id
        item['link'] = db_item.link
        item_list.append(item)

    return { 'item_list' : item_list }

@u403
@json
def j_subscription_item_show(request,subscription_id,item_id):
    pass

@u403
@json
def j_subscription_item_set_readdone(request,subscription_id,item_id,value):
    pass
