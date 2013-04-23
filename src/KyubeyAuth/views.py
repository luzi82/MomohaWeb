# Create your views here.
import django.core.exceptions
import KyubeyAuth.forms
import simplejson
import django.http
import django.shortcuts
import KyubeyAuth.cmds

def json(request):
    
    if request.method != "POST":
        raise django.core.exceptions.ValidationError("not POST")
    
    form = KyubeyAuth.forms.JsonForm(request.POST)
    if not form.is_valid():
        raise django.core.exceptions.ValidationError(form.errors)
    
    json = form.cleaned_data["json"]
    json = simplejson.loads(json)
    
    if json['cmd'] not in KyubeyAuth.cmds.cmd_dict:
        raise django.http.Http404
    
    f = KyubeyAuth.cmds.cmd_dict[json['cmd']]
    if f == None:
        raise django.http.Http404
    
    try:
        if 'argv' in json:
            ret = f(request,**(json['argv']))
        else:
            ret = f(request)
    except django.core.exceptions.ObjectDoesNotExist:
        raise django.http.Http404

    return django.http.HttpResponse(simplejson.dumps(ret), mimetype='application/json')


def cmd_js(request):

    return django.shortcuts.render(
        request,
        "KyubeyAuth/cmd.js.tmpl",
        {
            "cmd_list":KyubeyAuth.cmds.cmd_list
        },
        content_type="application/javascript"
    )
