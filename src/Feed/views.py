from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"index.html")

def addSubscription(request):
    pass

def rmSubscription(request):
    pass

def listSubscription(request):
    pass

def listSubscriptionContent(request):
    pass

def markRead(request):
    pass
