from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from django.template import RequestContext

from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf

