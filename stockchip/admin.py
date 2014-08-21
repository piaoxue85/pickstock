#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from stockchip.models import ChipDistridution

# 盈餘分配表(季)
class ChipDistridutionAdmin(admin.ModelAdmin):
	list_display = ('ID', 'date', 'symbol', 'bigchip_holders', 'bigchip_holdings',
					 'bigchip_percent', 'bigchip_monthly_change',
					 "modified_date")
	list_filter = ('date', 'symbol')
	search_fields = ('symbol', 'date')

admin.site.register(ChipDistridution, ChipDistridutionAdmin)