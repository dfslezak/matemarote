from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404

from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from django.views.static import serve
from django.conf import settings

import os
import sys

from users.models import UserProfile,UserProfileForm
from games.models import Game,GameRevision,GameFlowNode
from web_frontend.models import WEBGAMES_DIR,WEBGAMES_RES_DIR,WEBGAMES_GAMEFILES_DIR,WEBGAMES_SCREENSHOTS_DIR

class GameNotEnabled(Exception):
    pass

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
def gameflow(request):
    c = RequestContext(request)

    user = request.user.get_profile()
    gf = user.get_gameflow()
    
    skills = gf.list_games_per_skill(user.game_flow_status)
    skills_list = []
    
    for skill in sorted(skills.keys()):
        single_skill_list = []
        for (gfn,e) in skills[skill]:
            try:
                print gfn.__dict__
                tooltip = gfn.webgameflownode.get_tooltip(gf)
            except ObjectDoesNotExist:
                tooltip = ''
            single_skill_list.append([gfn,e,tooltip])
        skills_list.append(single_skill_list)
    print skills_list
    c['skill_list'] = skills_list
    
    return render_to_response('games/gameflow.html', c)
    
@login_required
def serve_game(request, game_flow_node):
    c = RequestContext(request)
    c.update(csrf(request))
    
    template = 'games/serve_game.html'

    # Check game name and version
    try:        
        user = request.user.get_profile()
        gf = user.get_gameflow()
        
        gfn = GameFlowNode.objects.get(pk=game_flow_node)
        if not gfn.game_flow == gf:
            raise ObjectDoesNotExist()
        
        if not gfn.is_enabled(user.game_flow_status):
            raise GameNotEnabled()
        #selected_game = Game.objects.get(name=game_name)
        selected_game_revision = gfn.game_revision
        
        print 'Found enabled game at skill level', gfn.skill_level, ' GAME: ', gfn.webgameflownode.display_name
                
    except IndexError as e:
        print "Unexpected error:", e
        template = 'games/wrong_url.html'
    except ObjectDoesNotExist as e:
        print "Unexpected error:", e
        template = 'games/wrong_url.html'
    except ValueError as e:
        print "Unexpected error:", e
        template = 'games/wrong_url.html'
    except GameNotEnabled as e:
        print "Unexpected error:", e
        template = 'games/game_disabled.html'
    
    return render_to_response(template,c)


def _serve_game_path(request, directory, filename):
    full_dir = os.path.join(settings.MEDIA_ROOT,WEBGAMES_DIR,directory)
    full_path = os.path.join(full_dir,filename)
    if not os.path.exists(full_path):
        raise Http404("File Not Found: %s" % (full_path))
    return serve(request, filename, document_root=full_dir)

def serve_game_resource(request, game_name, game_version, resource_path):
    return _serve_game_path(request, os.path.join(game_name,game_version,WEBGAMES_RES_DIR), resource_path)

def serve_game_file(request, game_name, game_version, game_file_path):
    return _serve_game_path(request, os.path.join(game_name,game_version,WEBGAMES_GAMEFILES_DIR), game_file_path)
