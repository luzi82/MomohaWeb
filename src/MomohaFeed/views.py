from MomohaFeed.forms import JsonForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
import MomohaFeed.cmds
import django.core.exceptions
import simplejson

#def index(request):
#
#    return render(request,"MomohaFeed/index.html")


def json(request):
    
    if request.method != "POST":
        raise django.core.exceptions.ValidationError("not POST")
    
    form = JsonForm(request.POST)
    if not form.is_valid():
        raise django.core.exceptions.ValidationError(form.errors)
    
    json = form.cleaned_data["json"]
    json = simplejson.loads(json)
    
    if json['cmd'] not in MomohaFeed.cmds.cmd_dict:
        raise Http404
    
    f = MomohaFeed.cmds.cmd_dict[json['cmd']]
    if f == None:
        raise Http404
    
    try:
        if 'argv' in json:
            ret = f(request,**(json['argv']))
        else:
            ret = f(request)
    except ObjectDoesNotExist:
        raise Http404

    return HttpResponse(simplejson.dumps(ret), mimetype='application/json')


def cmd_js(request):

    return render(request,"MomohaFeed/cmd.js.tmpl",{"cmd_list":MomohaFeed.cmds.cmd_list},content_type="application/javascript")
