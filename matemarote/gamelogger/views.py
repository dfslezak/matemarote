from django.db import models
from django.contrib.auth.models import User
from models import PlaySession,LogEntry
from django.contrib.auth.decorators import login_required,permission_required
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from games.models import GameFlowNode
import json
import StringIO
  
@login_required
def new_play_session(request):    
    if request.method == 'POST':
        try:            
            gfn = json.loads(request.POST['game_flow_node'])
            print 'game_flow_node:', gfn
            session = PlaySession.objects.create(user = request.user, game_flow_node = GameFlowNode.objects.get(pk=gfn), 
                                        ip = request.META['REMOTE_ADDR'])
            request.session['current_play_session'] = session.id
        
            response_data = {}
            response_data['sessionplay_id'] = session.id
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            print e
            return HttpResponse(status=500)
    return HttpResponse(status=200)
            
@login_required
def log_action(request):
    if request.method == 'POST':
        try:            
            play = get_object_or_404(PlaySession, pk=request.session['current_play_session'])
            print 'play session: ', play
    
            log = request.POST.get('log','')
            print 'log: ', log
            for line in StringIO.StringIO(log.encode('utf-8')):
                ev = json.JSONDecoder().decode(line)
                print 'ev',ev
                if 'time' in ev:
                    entry = LogEntry(session=play, log_code=ev['log_code'],
                                timestamp=ev['time'], order=ev['order'], _data='')
                else:
                    entry = LogEntry(session=play, log_code=ev['log_code'],
                                order=ev['order'], _data='')
                    
                entry.data = ev['data']
                entry.save()
    
        except Exception as e:
            print e
            return HttpResponse(status=500)
    return HttpResponse(status=200)
