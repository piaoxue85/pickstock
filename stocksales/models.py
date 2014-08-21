#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class MonthlySales(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    year = models.CharField(max_length=4, null=True)
    month = models.CharField(max_length=2, null=True)
    industry = models.CharField(max_length=20, null=True)
    symbol = models.CharField(max_length=8, null=True)
    cname = models.CharField(max_length=20, null=True)
    market = models.CharField(max_length=8, null=True)
    sales = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    sales_yoy = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    acc_sales = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    acc_sales_yoy = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.year, self.month,
                 self.symbol, self.cname, self.market, self.sales, self.sales_yoy, 
                 self.acc_sales, self.acc_sales_yoy, self.modified_date)
    class Meta:
        ordering = ['-market', 'symbol', 'year', 'month']
    class Admin:
        pass