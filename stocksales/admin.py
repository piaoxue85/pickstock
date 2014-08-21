#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from stocksales.models import MonthlySales

class MonthlySalesAdmin(admin.ModelAdmin):
	list_display = ("ID", "symbol", "cname", "market", "year", "month", 
					"sales", "sales_yoy", "acc_sales", "acc_sales_yoy", "modified_date")
	list_filter = ("market", "industry")
	search_fields = ("symbol", "cname")

# Register your models here.
admin.site.register(MonthlySales, MonthlySalesAdmin)