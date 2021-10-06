from django.shortcuts import redirect
from core.models import IgUser
from django.shortcuts import get_list_or_404, get_object_or_404


def session_not_exist(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            _u = request.session['username']
        except:
            _u = None

        if _u is not None:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper


def session_exist(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            _u = request.session['username']
        except:
            _u = None

        if _u is None:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('dash/')
    return wrapper