# Create your views here.
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def web(request):
    c = {}
    c.update(csrf(request))
    # ... view code here
    return render_to_response('base.html', c)
