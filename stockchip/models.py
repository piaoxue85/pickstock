#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class ChipDistridution(models.Model):
	ID = models.CharField(max_length=20, primary_key=True)
	symbol = models.CharField(max_length=20, db_index=True)
	# 資料日期-年
	year = models.CharField(max_length=4)
	# 資料日期-月
	month = models.CharField(max_length=2)
	# 資料日期
	date = models.CharField(max_length=6)
	# 持股分級1,000張以上的人數
	bigchip_holders = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持股分級1,000張以上的總持股股數
	bigchip_holdings = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持股分級1,000張以上佔集保庫存的比例
	bigchip_percent = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 持股分級1,000張以上的單月變動股數
	bigchip_monthly_change = models.DecimalField(max_digits=20, decimal_places=0, null=True)

	# 持股分級800~1,000張以上的人數
	bigchip_holders_2nd = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持股分級800~1,000張以上的總持股股數
	bigchip_holdings_2nd = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持股分級800~1,000張以上佔集保庫存的比例
	bigchip_percent_2nd = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 持股分級800~1,000張以上的單月變動股數
	bigchip_monthly_change_2nd = models.DecimalField(max_digits=20, decimal_places=0, null=True)

	# 持股分級600~800張以上的人數
	bigchip_holders_3rd = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持股分級600~800張以上的總持股股數
	bigchip_holdings_3rd = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持股分級600~800張以上佔集保庫存的比例
	bigchip_percent_3rd = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 持股分級600~800張以上的單月變動股數
	bigchip_monthly_change_3rd = models.DecimalField(max_digits=20, decimal_places=0, null=True)

	modified_date = models.DateField(auto_now=True)

	def __unicode__(self):
		return u'%s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.date,
			self.bigchip_holders, self.bigchip_holdings,self.bigchip_percent, self.bigchip_monthly_change,
			self.modified_date)
	class Meta:
		ordering = ['symbol', 'date']
	class Admin:
		pass