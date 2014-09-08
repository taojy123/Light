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

    checkall = request.REQUEST.get("checkall")
    check_1 = request.REQUEST.get("check_1")
    check_2 = request.REQUEST.get("check_2")
    check_3 = request.REQUEST.get("check_3")
    check_4 = request.REQUEST.get("check_4")
    if not (check_1 or check_2 or check_3 or check_4):
        checkall = "on"
    rs = []
    for r in qs.all():
        flag = False
        if checkall:
            flag = True
        if check_1 and r.is_1:
            flag = True
        if check_2 and r.is_2:
            flag = True
        if check_3 and r.is_3:
            flag = True
        if check_4 and r.is_4:
            flag = True
        if flag:
            rs.append(r)

    user = request.user

    return render_to_response('admin/query.html', locals())



def show_gps(request, **kw):
    id = request.REQUEST.get("id")
    unit = Unit.objects.get(id=id)
    gps = unit.gps
    gps = gps.encode("utf8")
    gps = gps.replace("：", ":").replace("，", ",").replace("，", ",").replace("'", "°").replace('"', "°")
    lon, lat = gps.strip().split(",")
    lon = lon.strip().split(":")[-1]
    lat = lat.strip().split(":")[-1]
    lons = lon.split("°")
    lats = lat.split("°")

    lon = 0
    if len(lons) > 1:
        lon += float(lons[0])
    if len(lons) > 2:
        lon += float(lons[1]) / 60
    if len(lons) > 3:
        lon += float(lons[2]) / 3600

    lat = 0
    if len(lats) > 1:
        lat += float(lats[0])
    if len(lats) > 2:
        lat += float(lats[1]) / 60
    if len(lats) > 3:
        lat += float(lats[2]) / 3600

    return render_to_response('show_gps.html', locals())






