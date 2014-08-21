#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from economics.models import TaiwanEconomicsIndicator

# 盈餘分配表(季)
class TaiwanEconomicsIndicatorAdmin(admin.ModelAdmin):
	list_display = ('date', 'twse_open', 'twse_high', 'twse_low', 'twse_close', 'twse_volumn', 'twse_pbr',
					 'monitoring_indicator', 'composite_leading_index', 'composite_leading_index_yoy',
					 'monetary_aggregates_M1B', 'monetary_aggregates_M1B_yoy',
					 "modified_date")
	list_filter = ('date', 'modified_date')
	search_fields = ('date', 'modified_date')

admin.site.register(TaiwanEconomicsIndicator, TaiwanEconomicsIndicatorAdmin)