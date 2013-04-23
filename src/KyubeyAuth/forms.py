import django.forms

class JsonForm (django.forms.Form):
    json = django.forms.CharField()
