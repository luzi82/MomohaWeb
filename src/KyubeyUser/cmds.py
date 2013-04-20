from django.core.exceptions import PermissionDenied
import inspect
from django.contrib.auth.models import User
import django.contrib.auth
from django.db.utils import IntegrityError
from django.conf import settings

cmd_list = []
cmd_dict = {}

def cmd(f):
    argv = inspect.getargspec(f)[0]
    argv = argv[1:]
    cmd_list.append({
         'name': f.func_name,
         'argv': argv,
    })
    cmd_dict[f.func_name]=f
    return f


def u403(f):
    def ff(request,*args,**kwargs):
        if request.user == None:
            raise PermissionDenied
        return f(request,*args,**kwargs)
    return ff


###########

@cmd
def add_user(request, username, password):
    
    if (len(password)<settings.KYUBEYUSER_PASSWORD_LENGTH_MIN):
        return {'success':False, 'reason':'password short'}
    
    try:
        User.objects.create_user(
            username = username ,
            password = password
        )
    except IntegrityError:
        return {'success':False, 'reason':'username exist'}
        
    user = django.contrib.auth.authenticate(
        username = username,
        password = password
    )
    
    if user is None:
        return {'success':False, 'reason':'create user fail'}

    if not user.is_active:
        return {'success':False, 'resaon':"user not active"}

    django.contrib.auth.login(request, user)
    return {'success':True}


@cmd
def login(request, username, password):
    user = django.contrib.auth.authenticate(
        username = username,
        password = password
    )

    if user is None:
        return {'success':False, 'reason':'login fail'}

    if not user.is_active:
        return {'success':False, 'resaon':"user not active"}

    django.contrib.auth.login(request, user)
    return {'success':True}


@u403
@cmd
def logout(request):
    django.contrib.auth.logout(request)
    return {'success':True}


@u403
@cmd
def user_set_password(request, old_password, new_password):
    if (len(new_password)<settings.KYUBEYUSER_PASSWORD_LENGTH_MIN):
        return {'success':False, 'reason':'new_password short'}
    
    if not request.user.check_password(old_password):
        return {'success':False, 'reason':'old_password fail'}
    
    request.user.set_password(new_password)
    request.user.save()
    return {'success':True}
