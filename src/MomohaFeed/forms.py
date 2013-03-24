from django import forms

class SubscriptionAddForm (forms.Form):
    url = forms.CharField(widget=forms.widgets.Textarea())
