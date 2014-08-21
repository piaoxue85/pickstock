#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class TaiwanEconomicsIndicator(models.Model):
	date = models.CharField(max_length=6, primary_key=True)
	twse_open =  models.DecimalField(max_digits=20, decimal_places=2, null=True)
	twse_high =  models.DecimalField(max_digits=20, decimal_places=2, null=True)
	twse_low =  models.DecimalField(max_digits=20, decimal_places=2, null=True)
	twse_close =  models.DecimalField(max_digits=20, decimal_places=2, null=True)
	twse_volumn =  models.DecimalField(max_digits=20, decimal_places=2, null=True)
	twse_pbr =  models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 景氣對策信號分數(分)
	monitoring_indicator = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 景氣領先指標綜合指數(點)
	composite_leading_index = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	composite_leading_index_yoy = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 貨幣總計數 M1B(十億元)
	monetary_aggregates_M1B = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	monetary_aggregates_M1B_yoy = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	modified_date = models.DateField(auto_now=True)

	def __unicode__(self):
		return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.date, self.twse_close, self.twse_pbr,
			self.monitoring_indicator, self.composite_leading_index,self.composite_leading_index_yoy,
			self.monetary_aggregates_M1B, self.monetary_aggregates_M1B_yoy,
			self.modified_date)
	class Meta:
		ordering = ['date', 'modified_date']
	class Admin:
		pass