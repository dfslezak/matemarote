from django.db import models
from django.contrib.auth.models import User
from models import PlaySession,LogEntry
from django.contrib.auth.decorators import login_required,permission_required
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from games.models import GameFlowNode
import json

def ajax_login_required(view_func):
    def wrap(request, *args, **kwargs):
        print 'ADENTRO WRAP'
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        json_ret = json.dumps({ 'not_authenticated': True })
        return HttpResponse(json_ret, mimetype='application/json')
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap
    
@ajax_login_required
def new_play_session(request, game_flow_node):    
    gfn = json.loads(game_flow_node)
    session = PlaySession.objects.create(user = request.user, game_flow_node = GameFlowNode.objects.get(pk=gfn), 
                                    ip = request.META['REMOTE_ADDR'])
    request.session['current_play_session'] = session.id
    
    response_data = {}
    response_data['sessionplay_id'] = session.id
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@ajax_login_required
def log_action(request, gfn):
    play = get_object_or_404(PlaySession, pk=request.session['current_play_session'])
    
    log = request.POST.get('log','')
    for line in StringIO(log.encode('utf-8')):
        ev = json.JSONDecoder().decode(line)
        entry = LogEntry(savedplay=play, type=ev['type'],
                         ms=ev['time'], order=ev['order'], _data='')
        entry.data = ev['data']
        entry.save()
    
    return HttpResponse(status=200)
