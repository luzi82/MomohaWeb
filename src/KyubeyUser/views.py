# Create your views here.
import django.core.exceptions
import KyubeyUser.forms
import simplejson
import django.http
import django.shortcuts
import KyubeyUser.cmds

def json(request):
    
    if request.method != "POST":
        raise django.core.exceptions.ValidationError("not POST")
    
    form = KyubeyUser.forms.JsonForm(request.POST)
    if not form.is_valid():
        raise django.core.exceptions.ValidationError(form.errors)
    
    json = form.cleaned_data["json"]
    json = simplejson.loads(json)
    
    if json['cmd'] not in KyubeyUser.cmds.cmd_dict:
        raise django.http.Http404
    
    f = KyubeyUser.cmds.cmd_dict[json['cmd']]
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
        "KyubeyUser/cmd.js.tmpl",
        {
            "cmd_list":KyubeyUser.cmds.cmd_list
        },
        content_type="application/javascript"
    )
