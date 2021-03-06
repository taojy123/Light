# -*- coding: utf-8 -*-

from django.db import models
from django.core import validators
import re
import datetime


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

    anum = models.CharField(max_length=255, verbose_name="档案号",
        validators=[
            validators.RegexValidator(re.compile('^[1234567890\[\]]+$'), '档案号只能为数字或包含[]', 'invalid')
        ]
    )
    rnum = models.CharField(max_length=255, verbose_name="检测报告编号")
    name = models.CharField(max_length=255, verbose_name="单位名称")
    address = models.CharField(max_length=255, verbose_name="单位地址")
    project_name = models.CharField(max_length=255, verbose_name="项目名称")
    project_address = models.CharField(max_length=255, verbose_name="项目地址")
    gps = models.CharField(max_length=255, verbose_name="GPS定位信息", blank=True , null=True)
    time = models.DateField(verbose_name="检测时间")        #可选日期
    contact_department = models.CharField(max_length=255, verbose_name="联系部门", blank=True , null=True)
    contact_person = models.CharField(max_length=255, verbose_name="联系人")
    contact_phone = models.CharField(max_length=255, verbose_name="联系电话",
        validators=[
            validators.RegexValidator(re.compile('^[1234567890]+$'), '联系电话只能填写数字', 'invalid')
        ]
    )   # 只能数字
    buildings = models.CharField(max_length=255, verbose_name="受检建（构）筑物名称及接地电阻")    #可多个
    category = models.CharField(max_length=255, verbose_name="防雷类别", default=u'一类', choices=CATEGORY_CHOICES)
    basis = models.CharField(max_length=255, verbose_name="检测依据")    #可多个
    weather = models.CharField(max_length=255, verbose_name="天气状况", default=u'晴', choices=WEATHER_CHOICES)
    instrument_num = models.CharField(max_length=255, verbose_name="检测仪器及编号")    #可多个
    conclusion = models.CharField(max_length=255, verbose_name="检测结论")
    validity = models.DateField(verbose_name="有效期")        #可选日期
    write_person = models.CharField(max_length=255, verbose_name="编制员")
    test_person = models.CharField(max_length=255, verbose_name="检测员",
        validators=[
            validators.RegexValidator(re.compile('^.+ .+$'), '需两名以上检测员,姓名间以空格分隔', 'invalid')
        ]
    )     #两名以上
    check_person = models.CharField(max_length=255, verbose_name="审核员")
    bill_person = models.CharField(max_length=255, verbose_name="计费员")
    bill_check = models.CharField(max_length=255, verbose_name="计费复核")
    amount = models.CharField(max_length=255, verbose_name="计费金额",
        validators=[
            validators.RegexValidator(re.compile('^[1234567890,\.]+$'), '只能输入数字', 'invalid')
        ]
    )
    approve_person = models.CharField(max_length=255, verbose_name="批准人")
    approve_time = models.DateField(verbose_name="批准日期")        #可选日期

    rnum1 = models.CharField(max_length=255, blank=True , null=True)
    rnum2 = models.CharField(max_length=255, blank=True , null=True)
    rnum3 = models.CharField(max_length=255, blank=True , null=True)
    rnum4 = models.CharField(max_length=255, blank=True , null=True)


    class Meta:
        verbose_name = "单位信息"
        verbose_name_plural = "单位信息"

    def __unicode__(self):
        return self.anum + " " + self.name

    def save(self, *args, **kw):
        r = re.findall(ur"\[(\d+)\](.+)-(\d+)-(.+)\u53f7", self.rnum)
        rnum1 = r[0][0]
        rnum2 = r[0][1]
        rnum3 = r[0][2]
        rnum4 = r[0][3]
        self.rnum1 = rnum1
        self.rnum2 = rnum2
        self.rnum3 = rnum3
        self.rnum4 = rnum4
        return super(Unit, self).save(*args, **kw)

    @property
    def is_1(self):
        return "-1-" in self.rnum

    @property
    def is_2(self):
        return "-2-" in self.rnum

    @property
    def is_3(self):
        return "-3-" in self.rnum

    @property
    def is_4(self):
        return "-4-" in self.rnum

    @property
    def is_expiring(self):
        today = datetime.date.today()
        week_later = today + datetime.timedelta(days=7)
        return week_later >= self.validity and not self.is_expired

    @property
    def is_expired(self):
        today = datetime.date.today()
        return today >= self.validity


class Remind(models.Model):
    unit = models.ForeignKey(Unit)
    is_show = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)



