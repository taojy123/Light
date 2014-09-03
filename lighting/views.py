# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import auth
from models import *
import os
import uuid
from django.template import RequestContext



def index(request, **kw):
#    a = request.POST.get("a")
#    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
    return HttpResponseRedirect("/admin")



def query(request, **kw):

    return render_to_response('index.html', locals(), context_instance=RequestContext(request))




