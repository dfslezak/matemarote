# Create your views here.
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from users.models import UserProfile,UserProfileForm
from django.forms.models import modelform_factory

def web(request):
    c = RequestContext(request)
    c.update(csrf(request))
    return render_to_response('base.html', c)

@login_required
def edit_profile(request):
    c = RequestContext(request)
    c.update(csrf(request))
    
    if request.method == 'POST': # If the form has been submitted...
        form = UserProfileForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form.save()
        else:
            print form.errors
            print form.__dict__
#        ret_val = redirect('/')
        c['form'] = form.clean()
        next_url = 'userprofile/edit-profile.html'
        ret_val = render_to_response(next_url, c)

    else:
        u = request.user
        (up,created) = UserProfile.objects.get_or_create(user=u)
        form = UserProfileForm(initial=up.__dict__)
        c['form'] = form
        next_url = 'userprofile/edit-profile.html'
        ret_val = render_to_response(next_url, c)

    return ret_val
    