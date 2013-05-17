from django.http import HttpResponse
from users.models import *
# Create your views here.

def gameflow(request):
    
    if request.user.is_authenticated():
        us = UserProfile.objects.get(user=request.user.pk)
        u = str(us)
    else:
        # Do something for anonymous users.
        u = str(request.user)
        
    html = "<html><body>%s</body></html>" % u
    return HttpResponse(html)