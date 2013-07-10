from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required,permission_required
from django.template import RequestContext, Template
from django.http import Http404,HttpResponse,HttpResponseRedirect

from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from django.views.static import serve
from django.conf import settings

import os
import sys
import datetime
import zipfile

from users.models import UserProfile,UserProfileForm
from games.models import Game,GameRevision,GameFlowNode
from web_frontend.models import GameForm,GameRevisionForm,UploadGameRevisionForm,GameRevisionWebPackage,WEBGAMES_DIR,WEBGAMES_RES_DIR,WEBGAMES_GAMEFILES_DIR,WEBGAMES_SCREENSHOTS_DIR

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
            ret_val = redirect('/accounts/profile')

        else:
            #print form.errors
            #print form.__dict__
            c['form'] = form
            template = 'userprofile/edit-profile.html'
            ret_val = render_to_response(template, c)

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
        ret_val = render_to_response(template, c)

    return ret_val

@permission_required('games.game_admin')
def gamelist(request):
    c = RequestContext(request)
    c.update(csrf(request))

    next_url = None
    if request.method == 'POST':
        next_url = request.POST.get('next', '/games/admin/')
        try:
            action = request.POST['buttons']
            if action == 'add-game':
                form = GameForm(data=request.POST) 
                if form.is_valid():
                    n = form.cleaned_data['name']
                    d = form.cleaned_data['description']
                    g = Game(name=n,description=d)
                    g.save()
                else: 
                    print form
                    raise Exception('Invalid data in new game form.')
            elif action == 'add-game-revision':
                form = GameRevisionForm(data=request.POST) 
                if form.is_valid():
                    g = Game.objects.get(name=request.POST['gameref'])
                    v = form.cleaned_data['version']
                    cd = datetime.datetime.now()
                    pv = form.cleaned_data['previous_version']
                    gr = GameRevision(game=g,version=v,creation_date=cd,previous_version=pv)
                    gr.save()
                else: 
                    print form
                    raise Exception('Invalid data in new game revision form.')
            elif action == 'upload':
                f = request.FILES
                inst = None
                if inst:
                    form = UploadGameRevisionForm(data=request.POST,files=request.FILES,instance=inst)
                else:
                    form = UploadGameRevisionForm(data=request.POST,files=request.FILES)
                    if form.is_valid():
                        gr = GameRevision.objects.get(pk=request.POST['upload-gamerevref'])
                        path = GameRevisionWebPackage.static_dir(gr)
                        zf = zipfile.ZipFile(form.cleaned_data['upload_file'], 'r')
                        if GameRevisionWebPackage.checkPackageNamelist(zf.namelist()):
                            zf.extractall(path)
                        else:
                            raise Exception('Invalid Zip for game version package.')
                    else:
                        print form
                        raise Exception('Invalid data in upload form.')

        except Exception as e:
            next_url = None 
            c['error_msg'] = str(e) 

    if next_url == None:
        games = Game.objects.all()
        c['games'] = games
        c['add_game_form'] = GameForm()
        c['add_game_revision_form'] = GameRevisionForm()
        c['upload_game_revision_form'] = UploadGameRevisionForm()
        ret_val = render_to_response('games/gamelist.html',c)
    else:
        ret_val = HttpResponseRedirect(next_url)

    return ret_val
                
@login_required
def gameflow(request):
    c = RequestContext(request)

    user = request.user.get_profile()
    gf = user.get_gameflow()
    
    skills = gf.list_games_per_skill(user.gameflow_status)
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
def serve_game(request, gameflow_node):
    c = RequestContext(request)
    c.update(csrf(request))
    
    template = 'games/serve_game.html'

    # Check game name and version
    try:        
        user = request.user.get_profile()
        gf = user.get_gameflow()
        
        gfn = GameFlowNode.objects.get(pk=gameflow_node)
        if not gfn.gameflow == gf:
            raise ObjectDoesNotExist()
        
        if not gfn.is_enabled(user.gameflow_status):
            raise GameNotEnabled()
        #selected_game = Game.objects.get(name=game_name)
        selected_game_revision = gfn.game_revision
        
        print 'Found enabled game at skill level', gfn.skill_level, ' GAME: ', gfn.webgameflownode.display_name
        print settings.MEDIA_ROOT
        template = os.path.join(gfn.webgameflownode.static_dir, 'pages/juego.html')
        
        
        c['seconds_played'] = 0
        c['gameflow_node'] = gameflow_node
        
        t = Template(open(template,'r').read())
        tr = t.render(c)
        
        return HttpResponse(tr)
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

def serve_game_resource(request, gameflow_node, resource_path):
    gfn = GameFlowNode.objects.get(pk=gameflow_node)
    return _serve_game_path(request, gfn.webgameflownode.resource_path, resource_path)

def serve_game_file(request, gameflow_node, game_file_path):
    gfn = GameFlowNode.objects.get(pk=gameflow_node)
    return _serve_game_path(request, gfn.webgameflownode.game_file_path, game_file_path)
