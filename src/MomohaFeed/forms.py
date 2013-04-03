import django.forms
import django.core.exceptions


class AddSubscriptionForm (django.forms.Form):
    url = django.forms.URLField()


class SubscriptionListItemForm (django.forms.Form):
    subscription_id = django.forms.IntegerField()


class post_form(object):
    
    def __init__(self, form_class):
        self.form_class = form_class
        
    def __call__(self, f):
        def ff(request,*args,**kwargs):
            if request.method == "POST":
                form = self.form_class(request.POST)
                if form.is_valid():
                    return f(request,*args,form=form,**kwargs)
            raise django.core.exceptions.ValidationError
        return ff
