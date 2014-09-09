# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db.models import Q
from models import *
import os
import uuid
import xlwt
import xlrd
import time
import datetime


def index(request, **kw):
#    a = request.POST.get("a")
#    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
    return HttpResponseRedirect("/admin")


@login_required
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

    if submit == "output":
        value = ""

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

    if submit == "output":
        workBook = xlwt.Workbook()
        workBook.add_sheet("unit")
        sheet = workBook.get_sheet(0)
        sheet.write(0, 0, u"档案号")
        sheet.write(0, 1, u"检测报告编号")
        sheet.write(0, 2, u"单位名称")
        sheet.write(0, 3, u"单位地址")
        sheet.write(0, 4, u"项目名称")
        sheet.write(0, 5, u"项目地址")
        sheet.write(0, 6, u"GPS定位信息")
        sheet.write(0, 7, u"检测时间")
        sheet.write(0, 8, u"联系部门")
        sheet.write(0, 9, u"联系人")
        sheet.write(0, 10, u"联系电话")
        sheet.write(0, 11, u"受检建（构）筑物名称及接地电阻")
        sheet.write(0, 12, u"防雷类别")
        sheet.write(0, 13, u"检测依据")
        sheet.write(0, 14, u"天气状况")
        sheet.write(0, 15, u"检测仪器及编号")
        sheet.write(0, 16, u"检测结论")
        sheet.write(0, 17, u"有效期")
        sheet.write(0, 18, u"编制员")
        sheet.write(0, 19, u"检测员")
        sheet.write(0, 20, u"审核员")
        sheet.write(0, 21, u"计费员")
        sheet.write(0, 22, u"计费复核")
        sheet.write(0, 23, u"计费金额")
        sheet.write(0, 24, u"批准人")
        sheet.write(0, 25, u"批准日期")
        sheet.write(0, 26, u"系统内部编号")
        i = 0
        for r in rs:
            i += 1
            sheet.write(i, 0, r.anum)
            sheet.write(i, 1, r.rnum)
            sheet.write(i, 2, r.name)
            sheet.write(i, 3, r.address)
            sheet.write(i, 4, r.project_name)
            sheet.write(i, 5, r.project_address)
            sheet.write(i, 6, r.gps)
            sheet.write(i, 7, r.time.strftime("'%Y-%m-%d"))
            sheet.write(i, 8, r.contact_department)
            sheet.write(i, 9, r.contact_person)
            sheet.write(i, 10, r.contact_phone)
            sheet.write(i, 11, r.buildings)
            sheet.write(i, 12, r.category)
            sheet.write(i, 13, r.basis)
            sheet.write(i, 14, r.weather)
            sheet.write(i, 15, r.instrument_num)
            sheet.write(i, 16, r.conclusion)
            sheet.write(i, 17, r.validity.strftime("'%Y-%m-%d"))
            sheet.write(i, 18, r.write_person)
            sheet.write(i, 19, r.test_person)
            sheet.write(i, 20, r.check_person)
            sheet.write(i, 21, r.bill_person)
            sheet.write(i, 22, r.bill_check)
            sheet.write(i, 23, r.amount)
            sheet.write(i, 24, r.approve_person)
            sheet.write(i, 25, r.approve_time.strftime("'%Y-%m-%d"))
            sheet.write(i, 26, r.id)
        filename = "unit_" + datetime.datetime.now().strftime("%Y%m%d%H%M%M") + ".xls"
        workBook.save("static/output/" + filename)
        time.sleep(1)
        return HttpResponseRedirect("/static/output/" + filename)

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


@login_required
def unit_detail(request, **kw):
    id = request.REQUEST.get("id")
    unit = Unit.objects.get(id=id)
    r = unit
    user = request.user
    return render_to_response('admin/unit_detail.html', locals())



@login_required
def management(request, **kw):
    user = request.user
    return render_to_response('admin/management.html', locals())

@csrf_exempt
@login_required
def input_unit(request, **kw):
    f = request.FILES.get("input_file")
    book = xlrd.open_workbook(f.name, file_contents=f.read())
    sheet = book.sheets()[0]
    nrows = sheet.nrows
    for i in range(1, nrows):
        items = sheet.row_values(i)
        id = items[26]
        if Unit.objects.filter(id=id):
            unit = Unit.objects.get(id=id)
        else:
            unit = Unit()
            unit.id = id
        unit.anum = items[0]
        unit.rnum = items[1]
        unit.name = items[2]
        unit.address = items[3]
        unit.project_name = items[4]
        unit.project_address = items[5]
        unit.gps = items[6]
        unit.time = datetime.datetime.strptime(items[7], "'%Y-%m-%d")
        unit.contact_department = items[8]
        unit.contact_person = items[9]
        unit.contact_phone = items[10]
        unit.buildings = items[11]
        unit.category = items[12]
        unit.basis = items[13]
        unit.weather = items[14]
        unit.instrument_num = items[15]
        unit.conclusion = items[16]
        unit.validity = datetime.datetime.strptime(items[17], "'%Y-%m-%d")
        unit.write_person = items[18]
        unit.test_person = items[19]
        unit.check_person = items[20]
        unit.bill_person = items[21]
        unit.bill_check = items[22]
        unit.amount = items[23]
        unit.approve_person = items[24]
        unit.approve_time = datetime.datetime.strptime(items[25], "'%Y-%m-%d")
        unit.save()
    return HttpResponse("<script>alert('导入成功');top.location.href='/'</script>")

