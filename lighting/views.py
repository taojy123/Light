# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import auth
from django.db.models import Q
from models import *
import os
import uuid
from django.template import RequestContext



def index(request, **kw):
#    a = request.POST.get("a")
#    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
    return HttpResponseRedirect("/admin")



def query(request, **kw):
    keys = request.REQUEST.getlist("keys")
    conditions = request.REQUEST.getlist("conditions")
    values = request.REQUEST.getlist("values")
    submit = request.REQUEST.get("submit")

    qs = Unit.objects.all()

    if submit == "search":
        keys = []
        conditions = []
        values = []

    for i in range(len(values)):
        key = keys[i]
        condition = conditions[i]
        value = values[i]
        if key and value:
            if condition == "==":
                qs = qs.filter(**{str(key+"__icontains") : value})
            elif condition == "!=":
                qs = qs.exclude(**{key+"__icontains" : value})

    key = request.REQUEST.get("key")
    condition = request.REQUEST.get("condition")
    value = request.REQUEST.get("value")
    if key and value:
        if condition == "==":
            qs = qs.filter(**{str(key+"__icontains") : value})
        elif condition == "!=":
            qs = qs.exclude(**{key+"__icontains" : value})
        keys.append(key)
        conditions.append(condition)
        values.append(value)

    rs = qs.all()

    return render_to_response('admin/query.html', locals())




