#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class StockID(models.Model):
    symbol = models.CharField(max_length=8, primary_key=True)
    cname = models.CharField(max_length=20)
    issuedate = models.DateField()
    market = models.CharField(max_length=8)
    industry = models.CharField(max_length=20)
    modified_date = models.DateField(auto_now=True)

    # 呼叫objects會自動傳回的欄位值
    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (self.symbol, self.cname,
                 self.issuedate, self.market, self.industry, self.modified_date)
    class Meta:
        ordering = ['-market','symbol']
    class Admin:
    	pass