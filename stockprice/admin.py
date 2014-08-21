#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from stockprice.models import StockPrice, LatestStockPrice

class StockPriceAdmin(admin.ModelAdmin):
	list_display = ('ID', 'symbol', 'year', 'month', 'p_open', 'p_high', 'p_low', 'p_close', 'avgdayvol', 'p_adjclose', "modified_date")
	list_filter = ("symbol", "year")
	search_fields = ('symbol', 'year')

# Register your models here.
admin.site.register(StockPrice, StockPriceAdmin)

class LatestStockPriceAdmin(admin.ModelAdmin):
	list_display = ('symbol', 'p_close', 'market', "modified_date")
	search_fields = ('symbol', 'market')

# Register your models here.
admin.site.register(LatestStockPrice, LatestStockPriceAdmin)