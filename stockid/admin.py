#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from stockid.models import StockID

class StockIDAdmin(admin.ModelAdmin):
	list_display = ["market", "symbol", "cname", "issuedate", "industry", "modified_date"]
	list_filter = ("market", "industry")
	search_fields = ("symbol", "cname")

# Register your models here.
admin.site.register(StockID, StockIDAdmin)