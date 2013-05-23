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
    return render_to_response('index/index.html', c)

@login_required
def view_profile(request):
    c = RequestContext(request)
    
    u = request.user
    profile = request.user.get_profile()
    c['profile'] = profile
    print profile.__dict__

    return render_to_response('userprofile/view-profile.html', c)

@login_required
def edit_profile(request):
    c = RequestContext(request)
    c.update(csrf(request))
    
    if request.method == 'POST': # If the form has been submitted, save and redirect.
        print '---------- SAVE AND REDIRECT -----------'
        form = UserProfileForm(data=request.POST,files=request.FILES,instance=request.user.get_profile()) 
        if form.is_valid():
            form.save()
            ret_val = redirect('/')
        else:
            print form.errors
            print form.__dict__
            c['form'] = form
            template = 'userprofile/edit-profile.html'
            ret_val = render_to_response(template, c)

    else: # Show form for edition
        print '---------- SHOW FOR EDITION -----------'
        print 'User: ', request.user
        u = request.user
        profile = request.user.get_profile()
        print 'Profile: ', profile
        
        form = UserProfileForm(instance=profile)
        print 'Form: ', form.as_p()
        c['form'] = form
        template = 'userprofile/edit-profile.html'
        ret_val = render_to_response(template, c)

    return ret_val
    