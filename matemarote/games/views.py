from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from django.template import RequestContext

from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf

@login_required
def gameflow(request):
    c = RequestContext(request)

    user = request.user.get_profile()
    gf = user.get_gameflow()
    
    sk = gf.list_games_per_skill(user.game_flow_status)
    sk_list = []
    
    for s in sorted(sk.keys()):
        sk_list.append(sk[s])
    c['skill_list'] = sk_list
    
    return render_to_response('games/gameflow.html', c)
