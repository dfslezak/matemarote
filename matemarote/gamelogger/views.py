from django.db import models
from django.contrib.auth.models import User
from models import PlaySession,LogEntry
from django.contrib.auth.decorators import login_required,permission_required
from django.http import Http404,HttpResponse,HttpResponseRedirect,get_object_or_404

import json

@login_required
def new_play(request, gfn):    
    session = PlaySession.objects.create(user = request.user, game_flow_node = gfn, 
                                    ip = request.META['REMOTE_ADDR'])
    request.session['current_play_session'] = session.id
    
    response_data['sessionplay_id'] = session.id
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
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
