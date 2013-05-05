import django.forms
#import django.core.exceptions

class JsonForm (django.forms.Form):
    json = django.forms.CharField()

class UploadForm (django.forms.Form):
    json = django.forms.CharField()
    file = django.forms.FileField() 

#class AddSubscriptionForm (django.forms.Form):
#    url = django.forms.URLField()
#
#
#class SubscriptionSetEnableForm (django.forms.Form):
#    subscription_id = django.forms.IntegerField()
#    value = django.forms.BooleanField(required = False)
#
#
#class SubscriptionListItemForm (django.forms.Form):
#    subscription_id = django.forms.IntegerField()
#
#
#class SubscriptionItemDetailForm (django.forms.Form):
#    subscription_id = django.forms.IntegerField()
#    item_id = django.forms.IntegerField()
#
#
#class SubscriptionItemSetReaddoneForm (django.forms.Form):
#    subscription_id = django.forms.IntegerField()
#    item_id = django.forms.IntegerField()
#    value = django.forms.BooleanField(required = False)
#
#
#class SubscriptionPollForm (django.forms.Form):
#    subscription_id = django.forms.IntegerField()


#class post_form(object):
#    
#    def __init__(self, form_class):
#        self.form_class = form_class
#        
#    def __call__(self, f):
#        def ff(request,*args,**kwargs):
#            if request.method == "POST":
#                form = self.form_class(request.POST)
#                if form.is_valid():
#                    return f(request,*args,form=form,**kwargs)
#                else:
#                    raise django.core.exceptions.ValidationError(form.errors)
#            raise django.core.exceptions.ValidationError("not POST")
#        return ff
