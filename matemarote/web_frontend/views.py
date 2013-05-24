from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from users.models import UserProfile,UserProfileForm
from games.models import Game,GameRevision
from django.views.static import serve
from os import path

import sys 

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
        #print '---------- SAVE AND REDIRECT -----------'
        form = UserProfileForm(data=request.POST,files=request.FILES,instance=request.user.get_profile()) 
        if form.is_valid():
            form.save()
            
            profile = request.user.get_profile()
            c['profile'] = profile
            ret_val = redirect('/accounts/profile',c)

        else:
            #print form.errors
            #print form.__dict__
            c['form'] = form
            template = 'userprofile/edit-profile.html'

    else: # Show form for edition
        #print '---------- SHOW FOR EDITION -----------'
        #print 'User: ', request.user
        u = request.user
        profile = request.user.get_profile()
        #print 'Profile: ', profile
        
        form = UserProfileForm(instance=profile)
        #print 'Form: ', form.as_p()
        c['form'] = form
        template = 'userprofile/edit-profile.html'

    return render_to_response(template, c)
    
@login_required
def serve_game(request):
    c = RequestContext(request)
    c.update(csrf(request))
    
    template = 'games/serve_game.html'

    # Check URL and get game
    url = request.get_full_path()
    url_tokens = url.split('/')
    try:
        ind = url_tokens.index('games')
        game_name = url_tokens[ind+1]
        game_version = url_tokens[ind+2]
        
        selected_game = Game.objects.get(name=game_name)
        selected_game_revision = GameRevision.objects.get(game=selected_game, version=game_version)        

        # Check permission based on gameflow.
        user = request.user.get_profile()
        gf = user.get_gameflow()
        game_list = gf.list_games_per_skill(user.game_flow_status)
        print game_list
        
        for sk in game_list.keys():
            level = game_list[sk]
            game_tuple = [game for (game,enabled) in level if game == selected_game_revision.pk and enabled]
            
            if len(game_tuple)>0:
                print 'Found enabled game at skill level', sk, ' GAME: ', game_tuple[0]
                
    except IndexError as e:
        print "Unexpected error:", e
        template = 'games/wrong_url.html'
    except ObjectDoesNotExist as e:
        print "Unexpected error:", e
        template = 'games/wrong_url.html'
    
    return render_to_response(template,c)


def _serve_game_path(request, directory, filename):
    if not path.exists(settings.MEDIA_ROOT+directory+filename):
        raise Http404("File Not Found")
    return serve(request, filename, document_root=settings.MEDIA_ROOT+directory)

def serve_game_resource(request, game_name, resource_path):
    return _serve_game_path(request, request.game.resource_path, resource_path)

def serve_game_file(request, game_name, game_file_path):
    return _serve_game_path(request, request.game.game_file_path, game_file_path)
