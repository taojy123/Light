# -*- coding: utf-8 -*-

from django.db import models


class Unit(models.Model):

    CATEGORY_CHOICES = (
        (u'一类', u"一类"),
        (u'二类', u"二类"),
        (u'三类', u"三类"),
        )

    WEATHER_CHOICES = (
        (u'晴', u"晴"),
        (u'多云', u"多云"),
        (u'阴', u"阴"),
        (u'雨', u"雨"),
        )

    anum = models.CharField(max_length=255, verbose_name="档案号")
    rnum = models.CharField(max_length=255, verbose_name="检测报告编号")
    name = models.CharField(max_length=255, verbose_name="单位名称")
    address = models.CharField(max_length=255, verbose_name="单位地址")
    project_name = models.CharField(max_length=255, verbose_name="项目名称")
    project_address = models.CharField(max_length=255, verbose_name="项目地址")
    gps = models.CharField(max_length=255, verbose_name="GPS定位信息", blank=True , null=True)
    time = models.DateField(verbose_name="检测时间")        #可选日期
    contact_department = models.CharField(max_length=255, verbose_name="联系部门", blank=True , null=True)
    contact_person = models.CharField(max_length=255, verbose_name="联系人")
    contact_phone = models.CharField(max_length=255, verbose_name="联系电话")   # 只能数字
    buildings = models.CharField(max_length=255, verbose_name="受检建（构）筑物名称及接地电阻")    #可多个
    category = models.CharField(max_length=255, verbose_name="防雷类别", default=u'一类', choices=CATEGORY_CHOICES)
    basis = models.CharField(max_length=255, verbose_name="检测依据")    #可多个
    weather = models.CharField(max_length=255, verbose_name="天气状况", default=u'晴', choices=WEATHER_CHOICES)
    instrument_num = models.CharField(max_length=255, verbose_name="检测仪器及编号")    #可多个
    conclusion = models.CharField(max_length=255, verbose_name="检测结论")
    validity = models.DateField(verbose_name="有效期")        #可选日期
    write_person = models.CharField(max_length=255, verbose_name="编制员")
    test_person = models.CharField(max_length=255, verbose_name="检测员")     #两名以上
    check_person = models.CharField(max_length=255, verbose_name="审核员")
    bill_person = models.CharField(max_length=255, verbose_name="计费员")
    bill_check = models.CharField(max_length=255, verbose_name="计费复核")
    amount = models.CharField(max_length=255, verbose_name="计费金额")
    approve_person = models.CharField(max_length=255, verbose_name="批准人")
    approve_time = models.DateField(verbose_name="批准日期")        #可选日期


    class Meta:
        verbose_name = "单位信息"
        verbose_name_plural = "单位信息"

    def __unicode__(self):
        return self.anum + " " + self.name



