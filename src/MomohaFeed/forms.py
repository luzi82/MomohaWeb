from django import forms

class SubscriptionAddForm (forms.Form):
    url = forms.URLField()
