from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    # TODO
    return render(request,"dummy.tmpl")

@login_required
def listSubscription(request):
    # TODO
    return render(request,"dummy.tmpl")

@login_required
def subscriptionAdd(request):
    if request.method == "POST":
        # TODO
        return render(request,"dummy.tmpl")
    else:
        # TODO
        return render(request,"dummy.tmpl")

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
