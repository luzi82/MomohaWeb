from django import forms

class SubscriptionAddForm (forms.Form):
    url = forms.URLField()

class SubscriptionListItemForm (forms.Form):
    subscription_id = forms.IntegerField()
