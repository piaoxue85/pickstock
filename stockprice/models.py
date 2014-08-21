#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class StockPrice(models.Model):
	ID = models.CharField(max_length=20, primary_key=True)
	symbol = models.CharField(max_length=8)
	year = models.CharField(max_length=4)
	month = models.CharField(max_length=2)
	p_open = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	p_high = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	p_low = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	p_close = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	avgdayvol = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	p_adjclose = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	modified_date = models.DateField(auto_now=True)

	def __unicode__(self):
		return u'%s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.year, self.month,
			self.p_open, self.p_high, self.p_low, self.p_close, self.avgdayvol, self.p_adjclose,
			self.modified_date)
	class Meta:
		ordering = ['symbol', '-year', '-month']
	class Admin:
		pass

class LatestStockPrice(models.Model):
	symbol = models.CharField(max_length=8, primary_key=True)
	p_close = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	market = models.CharField(max_length=3)
	modified_date = models.DateField(auto_now=True)

	def __unicode__(self):
		return u'%s %s %s' % (self.symbol, self.p_close, self.market, self.modified_date)
	class Meta:
		ordering = ['symbol', 'market']
	class Admin:
		pass