from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import *
from datetime import date
# Create your views here.

@login_required
def gameflow(request):
    (us,created) = UserProfile.objects.get_or_create(user=request.user,defaults={'birthdate': date(1970, 01, 01),'gender':1,'handedness':1})
    u = us.user

    html = "<html><body>User: %s<br><br>GameFlows: %s</body></html>" % (u,us.program.game_flow.list_games_per_skill(us.game_flow_status))
    return HttpResponse(html)
