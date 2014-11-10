#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from datetime import date, datetime
import json

import pdb
from stockid.models import StockID
from stockprice.models import StockPrice, LatestStockPrice
from stocksales.models import MonthlySales
from stockfins.models import SeasonBalanceSheet, SeasonIncomeStatement, SeasonCashFlow, SeasonFinancialRatio
from stockfins.models import AnnualIncomeStatement, AnnualCashFlow, AnnualFinancialRatio, EarningsPayout
from stockchip.models import ChipDistridution
from economics.models import TaiwanEconomicsIndicator

def home(request):
	return render_to_response("home.html")

def update(request):
	# 股票代號表
	id_latest = StockID.objects.order_by("-modified_date")[0:1].get()
	id_modified_date = id_latest.modified_date
	id_modified_count = StockID.objects.filter(modified_date = id_modified_date).count()
	id_all_count = StockID.objects.all().count()
	id_sii_count = StockID.objects.filter(market = "sii").count()
	id_otc_count = StockID.objects.filter(market = "otc").count()
	# 月營收表
	sales_latest = MonthlySales.objects.order_by("-modified_date")[0:1].get()
	sales_modified_date = sales_latest.modified_date
	sales_modified_count = MonthlySales.objects.filter(modified_date = sales_modified_date).count()
	sales_all_count = MonthlySales.objects.all().count()
	sales_latest = MonthlySales.objects.order_by("-year", "-month")[0:1].get()
	sales_modified_year_month = str(sales_latest.year) + "-" + str(sales_latest.month)
	sales_modified_year_month_count = MonthlySales.objects.filter(year = sales_latest.year, month = sales_latest.month).count()
	# 股價行情(月)
	price_latest = StockPrice.objects.order_by("-modified_date")[0:1].get()
	price_modified_date = price_latest.modified_date
	price_modified_count = StockPrice.objects.filter(modified_date = price_modified_date).count()
	price_all_count = StockPrice.objects.all().count()
	price_latest = StockPrice.objects.order_by("-year", "-month")[0:1].get()
	price_modified_year_month = str(price_latest.year) + "-" + str(price_latest.month)
	price_modified_year_month_count = StockPrice.objects.filter(year = price_latest.year, month = price_latest.month).count()
	# 股價行情(日)
	if LatestStockPrice.objects.count() == 0:
		dailyPrice_modified_date = None 
		dailyPrice_modified_count = None
		dailyPrice_all_count =None
		dailyPrice_sii_count = None 
		dailyPrice_otc_count = None
	else:
		dailyPrice_latest = LatestStockPrice.objects.order_by("-modified_date")[0:1].get()
		dailyPrice_modified_date = dailyPrice_latest.modified_date
		dailyPrice_modified_count = LatestStockPrice.objects.filter(modified_date = dailyPrice_modified_date).count()
		dailyPrice_all_count = LatestStockPrice.objects.all().count()
		dailyPrice_sii_count = LatestStockPrice.objects.filter(market = "sii").count()
		dailyPrice_otc_count = LatestStockPrice.objects.filter(market = "otc").count()
	# 財報－資產負債表（季）
	if SeasonBalanceSheet.objects.count() == 0:
		seasonBS_modified_date = None 
		seasonBS_modified_count = None
		seasonBS_all_count =None
		seasonBS_modified_year_season = None 
		seasonBS_modified_year_season_count = None
	else:
		seasonBS_latest = SeasonBalanceSheet.objects.order_by("-modified_date")[0:1].get()
		seasonBS_modified_date = seasonBS_latest.modified_date
		seasonBS_modified_count = SeasonBalanceSheet.objects.filter(modified_date = seasonBS_modified_date).count()
		seasonBS_all_count = SeasonBalanceSheet.objects.all().count()
		seasonBS_latest = SeasonBalanceSheet.objects.order_by("-year", "-season")[0:1].get()
		seasonBS_modified_year_season = str(seasonBS_latest.year) + "-" + str(seasonBS_latest.season)
		seasonBS_modified_year_season_count = SeasonBalanceSheet.objects.filter(year = seasonBS_latest.year, season = seasonBS_latest.season).count()
	
	# 財報－損益表（季）
	if SeasonIncomeStatement.objects.count() == 0:
		seasonIS_modified_date = None 
		seasonIS_modified_count = None
		seasonIS_all_count =None
		seasonIS_modified_year_season = None 
		seasonIS_modified_year_season_count = None
	else:
		seasonIS_latest = SeasonIncomeStatement.objects.order_by("-modified_date")[0:1].get()
		seasonIS_modified_date = seasonIS_latest.modified_date
		seasonIS_modified_count = SeasonIncomeStatement.objects.filter(modified_date = seasonIS_modified_date).count()
		seasonIS_all_count = SeasonIncomeStatement.objects.all().count()
		seasonIS_latest = SeasonIncomeStatement.objects.order_by("-year", "-season")[0:1].get()
		seasonIS_modified_year_season = str(seasonIS_latest.year) + "-" + str(seasonIS_latest.season)
		seasonIS_modified_year_season_count = SeasonIncomeStatement.objects.filter(year = seasonIS_latest.year, season = seasonIS_latest.season).count()
	
	# 財報－損益表（年）
	if AnnualIncomeStatement.objects.count() == 0:
		annualIS_modified_date = None 
		annualIS_modified_count = None
		annualIS_all_count =None
		annualIS_modified_year = None 
		annualIS_modified_year_count = None
	else:
		annualIS_latest = AnnualIncomeStatement.objects.order_by("-modified_date")[0:1].get()
		annualIS_modified_date = annualIS_latest.modified_date
		annualIS_modified_count = AnnualIncomeStatement.objects.filter(modified_date = annualIS_modified_date).count()
		annualIS_all_count = AnnualIncomeStatement.objects.all().count()
		annualIS_latest = AnnualIncomeStatement.objects.order_by("-year")[0:1].get()
		annualIS_modified_year = str(annualIS_latest.year)
		annualIS_modified_year_count = AnnualIncomeStatement.objects.filter(year = annualIS_latest.year).count()
	
	# 財報－現金流量表（季）
	if SeasonCashFlow.objects.count() == 0:
		seasonCF_modified_date = None 
		seasonCF_modified_count = None
		seasonCF_all_count =None
		seasonCF_modified_year_season = None 
		seasonCF_modified_year_season_count = None
	else:
		seasonCF_latest = SeasonCashFlow.objects.order_by("-modified_date")[0:1].get()
		seasonCF_modified_date = seasonCF_latest.modified_date
		seasonCF_modified_count = SeasonCashFlow.objects.filter(modified_date = seasonCF_modified_date).count()
		seasonCF_all_count = SeasonCashFlow.objects.all().count()
		seasonCF_latest = SeasonCashFlow.objects.order_by("-year", "-season")[0:1].get()
		seasonCF_modified_year_season = str(seasonCF_latest.year) + "-" + str(seasonCF_latest.season)
		seasonCF_modified_year_season_count = SeasonCashFlow.objects.filter(year = seasonCF_latest.year, season = seasonCF_latest.season).count()
	
	# 財報－現金流量表（年）
	if AnnualCashFlow.objects.count() == 0:
		annualCF_modified_date = None 
		annualCF_modified_count = None
		annualCF_all_count =None
		annualCF_modified_year = None 
		annualCF_modified_year_count = None
	else:
		annualCF_latest = AnnualCashFlow.objects.order_by("-modified_date")[0:1].get()
		annualCF_modified_date = annualCF_latest.modified_date
		annualCF_modified_count = AnnualCashFlow.objects.filter(modified_date = annualCF_modified_date).count()
		annualCF_all_count = AnnualCashFlow.objects.all().count()
		annualCF_latest = AnnualCashFlow.objects.order_by("-year")[0:1].get()
		annualCF_modified_year = str(annualCF_latest.year)
		annualCF_modified_year_count = AnnualCashFlow.objects.filter(year = annualCF_latest.year).count()

	# 財報－財務比率表（季）
	if SeasonFinancialRatio.objects.count() == 0:
		seasonFR_modified_date = None 
		seasonFR_modified_count = None
		seasonFR_all_count =None
		seasonFR_modified_year_season = None 
		seasonFR_modified_year_season_count = None
	else:
		seasonFR_latest = SeasonFinancialRatio.objects.order_by("-modified_date")[0:1].get()
		seasonFR_modified_date = seasonFR_latest.modified_date
		seasonFR_modified_count = SeasonFinancialRatio.objects.filter(modified_date = seasonFR_modified_date).count()
		seasonFR_all_count = SeasonFinancialRatio.objects.all().count()
		seasonFR_latest = SeasonFinancialRatio.objects.order_by("-year", "-season")[0:1].get()
		seasonFR_modified_year_season = str(seasonFR_latest.year) + "-" + str(seasonFR_latest.season)
		seasonFR_modified_year_season_count = SeasonFinancialRatio.objects.filter(year = seasonFR_latest.year, season = seasonFR_latest.season).count()
	
	# 財報－財務比率表（年）
	if AnnualFinancialRatio.objects.count() == 0:
		annualFR_modified_date = None 
		annualFR_modified_count = None
		annualFR_all_count =None
		annualFR_modified_year = None 
		annualFR_modified_year_count = None
	else:
		annualFR_latest = AnnualFinancialRatio.objects.order_by("-modified_date")[0:1].get()
		annualFR_modified_date = annualFR_latest.modified_date
		annualFR_modified_count = AnnualFinancialRatio.objects.filter(modified_date = annualFR_modified_date).count()
		annualFR_all_count = AnnualFinancialRatio.objects.all().count()
		annualFR_latest = AnnualFinancialRatio.objects.order_by("-year")[0:1].get()
		annualFR_modified_year = str(annualFR_latest.year)
		annualFR_modified_year_count = AnnualFinancialRatio.objects.filter(year = annualFR_latest.year).count()

	# 盈餘分配表(年)
	if EarningsPayout.objects.count() == 0:
		earningsPayout_modified_date = None 
		earningsPayout_modified_count = None
		earningsPayout_all_count =None
		earningsPayout_modified_year = None 
		earningsPayout_modified_year_count = None
	else:
		earningsPayout_latest = EarningsPayout.objects.order_by("-modified_date")[0:1].get()
		earningsPayout_modified_date = earningsPayout_latest.modified_date
		earningsPayout_modified_count = EarningsPayout.objects.filter(modified_date = earningsPayout_modified_date).count()
		earningsPayout_all_count = EarningsPayout.objects.all().count()
		earningsPayout_latest = EarningsPayout.objects.order_by("-year")[0:1].get()
		earningsPayout_modified_year = str(earningsPayout_latest.year)
		earningsPayout_modified_year_count = EarningsPayout.objects.filter(year = earningsPayout_latest.year).count()

	# 籌碼－資產負債表（季）
	if ChipDistridution.objects.count() == 0:
		monthChip_modified_date = None 
		monthChip_modified_count = None
		monthChip_all_count =None
		monthChip_modified_year_month = None 
		monthChip_modified_year_month_count = None
	else:
		monthChip_latest = ChipDistridution.objects.order_by("-modified_date")[0:1].get()
		monthChip_modified_date = monthChip_latest.modified_date
		monthChip_modified_count = ChipDistridution.objects.filter(modified_date = monthChip_modified_date).count()
		monthChip_all_count = ChipDistridution.objects.all().count()
		monthChip_latest = ChipDistridution.objects.order_by("-year", "-month")[0:1].get()
		monthChip_modified_year_month = str(monthChip_latest.year) + "-" + str(monthChip_latest.month)
		monthChip_modified_year_month_count = ChipDistridution.objects.filter(date = monthChip_latest.date).count()

	# 總經－台灣景氣指標（月）
	if TaiwanEconomicsIndicator.objects.count() == 0:
		monthTWindicator_modified_date = None
		monthTWindicator_modified_count = None
		monthTWindicator_all_count =None
		monthTWindicator_latest_date =None
		monthTWindicator_oldest_date =None
	else:
		monthTWindicator_latest = TaiwanEconomicsIndicator.objects.order_by("-modified_date")[0:1].get()
		monthTWindicator_modified_date = monthTWindicator_latest.modified_date
		monthTWindicator_modified_count = TaiwanEconomicsIndicator.objects.filter(modified_date = monthTWindicator_modified_date).count()
		monthTWindicator_all_count = TaiwanEconomicsIndicator.objects.all().count()
		monthTWindicator_latest = TaiwanEconomicsIndicator.objects.order_by("-date")[0:1].get()
		monthTWindicator_latest_date = str(monthTWindicator_latest.date)[:4] + "-" + str(monthTWindicator_latest.date)[4:]
		monthTWindicator_oldest = TaiwanEconomicsIndicator.objects.order_by("date")[0:1].get()
		monthTWindicator_oldest_date = str(monthTWindicator_oldest.date)[:4] + "-" + str(monthTWindicator_oldest.date)[4:]


	return render_to_response("update.html", {
		"id_modified_date":datetime.strftime(id_modified_date, '%Y-%m-%d'),
		"id_modified_count":id_modified_count,
		"id_all_count":id_all_count,
		"id_sii_count":id_sii_count,
		"id_otc_count":id_otc_count,

		"sales_modified_date":datetime.strftime(sales_modified_date, '%Y-%m-%d'),
		"sales_modified_count":sales_modified_count,
		"sales_all_count":sales_all_count,
		"sales_modified_year_month":sales_modified_year_month,
		"sales_modified_year_month_count":sales_modified_year_month_count,

		"price_modified_date":datetime.strftime(price_modified_date, '%Y-%m-%d'),
		"price_modified_count":price_modified_count,
		"price_all_count":price_all_count,
		"price_modified_year_month":price_modified_year_month,
		"price_modified_year_month_count":price_modified_year_month_count,

		"dailyPrice_modified_date":datetime.strftime(dailyPrice_modified_date, '%Y-%m-%d'),
		# "dailyPrice_modified_date":datetime.strftime(date.today(), '%Y-%m-%d'),
		"dailyPrice_modified_count":dailyPrice_modified_count,
		"dailyPrice_all_count":dailyPrice_all_count,
		"dailyPrice_sii_count":dailyPrice_sii_count,
		"dailyPrice_otc_count":dailyPrice_otc_count,

		"seasonBS_modified_date":datetime.strftime(seasonBS_modified_date, '%Y-%m-%d'),
		"seasonBS_modified_count":seasonBS_modified_count,
		"seasonBS_all_count":seasonBS_all_count,
		"seasonBS_modified_year_season":seasonBS_modified_year_season,
		"seasonBS_modified_year_season_count":seasonBS_modified_year_season_count,

		"seasonIS_modified_date":datetime.strftime(seasonIS_modified_date, '%Y-%m-%d'),
		"seasonIS_modified_count":seasonIS_modified_count,
		"seasonIS_all_count":seasonIS_all_count,
		"seasonIS_modified_year_season":seasonIS_modified_year_season,
		"seasonIS_modified_year_season_count":seasonIS_modified_year_season_count,

		"annualIS_modified_date":datetime.strftime(annualIS_modified_date, '%Y-%m-%d'),
		"annualIS_modified_count":annualIS_modified_count,
		"annualIS_all_count":annualIS_all_count,
		"annualIS_modified_year":annualIS_modified_year,
		"annualIS_modified_year_count":annualIS_modified_year_count,

		"seasonCF_modified_date":datetime.strftime(seasonCF_modified_date, '%Y-%m-%d'),
		"seasonCF_modified_count":seasonCF_modified_count,
		"seasonCF_all_count":seasonCF_all_count,
		"seasonCF_modified_year_season":seasonCF_modified_year_season,
		"seasonCF_modified_year_season_count":seasonCF_modified_year_season_count,

		"annualCF_modified_date":datetime.strftime(annualCF_modified_date, '%Y-%m-%d'),
		"annualCF_modified_count":annualCF_modified_count,
		"annualCF_all_count":annualCF_all_count,
		"annualCF_modified_year":annualCF_modified_year,
		"annualCF_modified_year_count":annualCF_modified_year_count,

		"seasonFR_modified_date":datetime.strftime(seasonFR_modified_date, '%Y-%m-%d'),
		"seasonFR_modified_count":seasonFR_modified_count,
		"seasonFR_all_count":seasonFR_all_count,
		"seasonFR_modified_year_season":seasonFR_modified_year_season,
		"seasonFR_modified_year_season_count":seasonFR_modified_year_season_count,

		"annualFR_modified_date":datetime.strftime(annualFR_modified_date, '%Y-%m-%d'),
		"annualFR_modified_count":annualFR_modified_count,
		"annualFR_all_count":annualFR_all_count,
		"annualFR_modified_year":annualFR_modified_year,
		"annualFR_modified_year_count":annualFR_modified_year_count,

		"earningsPayout_modified_date":datetime.strftime(earningsPayout_modified_date, '%Y-%m-%d'),
		"earningsPayout_modified_count":earningsPayout_modified_count,
		"earningsPayout_all_count":earningsPayout_all_count,
		"earningsPayout_modified_year":earningsPayout_modified_year,
		"earningsPayout_modified_year_count":earningsPayout_modified_year_count,

		"monthChip_modified_date":datetime.strftime(monthChip_modified_date, '%Y-%m-%d'),
		"monthChip_modified_count":monthChip_modified_count,
		"monthChip_all_count":monthChip_all_count,
		"monthChip_modified_year_month":monthChip_modified_year_month,
		"monthChip_modified_year_month_count":monthChip_modified_year_month_count,

		"monthTWindicator_modified_date":datetime.strftime(monthTWindicator_modified_date, '%Y-%m-%d'),
		"monthTWindicator_modified_count":monthTWindicator_modified_count,
		"monthTWindicator_all_count":monthTWindicator_all_count,
		"monthTWindicator_latest_date":monthTWindicator_latest_date,
		"monthTWindicator_oldest_date":monthTWindicator_oldest_date,
		})

def assign_task(request):
	if request.GET.get('q', '') and request.GET.get('button', ''):
		symbol = request.GET['q']
		task = request.GET['button']
		if StockID.objects.filter(symbol=symbol):
			request.session['symbol'] = symbol
			cname = StockID.objects.get(symbol=symbol).cname
			table_title = cname + "(" + str(symbol) + ")"
			#依照工作類別指派網頁
			if task == "Search_sales":
				return render_to_response('sales_tracking.html', {"table_title": table_title, "symbol":symbol})
			elif task == "Search_chips":
				return render_to_response('chip_tracking.html', {"table_title": table_title, "symbol":symbol})
			elif task == "Search_finrpts":
				return render_to_response('stock_overview.html', {"table_title": table_title, "symbol":symbol})
			else:
				return render_to_response('msg_error.html')
		else:
			return render_to_response('msg_error.html')
	else:
		return render_to_response('home.html')

def sales_overview(request):
	try:
		symbol = request.session['symbol']
	except:
		symbol = '2330'

	# 找出最新營收的年份是哪一年
	if datetime.today().month == 1:
		thisyear = int(datetime.today().year - 1)
	else:
		thisyear = int(datetime.today().year)

	cname = StockID.objects.filter(symbol=symbol).values_list('cname',flat=True)[0]
	monthly_sales = MonthlySales.objects.filter(symbol=symbol)
	# 抓出最近五年的營收/年增率/累積營收/累積營收年增率，並按月份排序
	data_yr0 = monthly_sales.filter(year=thisyear).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	data_yr1 = monthly_sales.filter(year=thisyear-1).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	data_yr2 = monthly_sales.filter(year=thisyear-2).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	data_yr3 = monthly_sales.filter(year=thisyear-3).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	data_yr4 = monthly_sales.filter(year=thisyear-4).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	# 宣告空的串列準備填入五年的資料
	sales_yr0 = ["","","","","","","","","","","",""]
	sales_yr1 = ["","","","","","","","","","","",""]
	sales_yr2 = ["","","","","","","","","","","",""]
	sales_yr3 = ["","","","","","","","","","","",""]
	sales_yr4 = ["","","","","","","","","","","",""]
	sales_yoy_yr0 = ["","","","","","","","","","","",""]
	sales_yoy_yr1 = ["","","","","","","","","","","",""]
	sales_yoy_yr2 = ["","","","","","","","","","","",""]
	sales_yoy_yr3 = ["","","","","","","","","","","",""]
	sales_yoy_yr4 = ["","","","","","","","","","","",""]
	acc_sales_yr0 = ["","","","","","","","","","","",""]
	acc_sales_yr1 = ["","","","","","","","","","","",""]
	acc_sales_yr2 = ["","","","","","","","","","","",""]
	acc_sales_yr3 = ["","","","","","","","","","","",""]
	acc_sales_yr4 = ["","","","","","","","","","","",""]
	acc_sales_yoy_yr0 = ["","","","","","","","","","","",""]
	acc_sales_yoy_yr1 = ["","","","","","","","","","","",""]
	acc_sales_yoy_yr2 = ["","","","","","","","","","","",""]
	acc_sales_yoy_yr3 = ["","","","","","","","","","","",""]
	acc_sales_yoy_yr4 = ["","","","","","","","","","","",""]

	for j in reversed(range(len(data_yr0))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr0[j][0]) == i+1:
				sales_yr0[i] = int(data_yr0[j][1])
				sales_yoy_yr0[i] = float(data_yr0[j][2])
				acc_sales_yr0[i] = int(data_yr0[j][3])
				acc_sales_yoy_yr0[i] = float(data_yr0[j][4])
				break
	for j in reversed(range(len(data_yr1))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr1[j][0]) == i+1:
				sales_yr1[i] = int(data_yr1[j][1])
				sales_yoy_yr1[i] = float(data_yr1[j][2])
				acc_sales_yr1[i] = int(data_yr1[j][3])
				acc_sales_yoy_yr1[i] = float(data_yr1[j][4])
				break
	for j in reversed(range(len(data_yr2))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr2[j][0]) == i+1:
				sales_yr2[i] = int(data_yr2[j][1])
				sales_yoy_yr2[i] = float(data_yr2[j][2])
				acc_sales_yr2[i] = int(data_yr2[j][3])
				acc_sales_yoy_yr2[i] = float(data_yr2[j][4])
				break
	for j in reversed(range(len(data_yr3))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr3[j][0]) == i+1:
				sales_yr3[i] = int(data_yr3[j][1])
				sales_yoy_yr3[i] = float(data_yr3[j][2])
				acc_sales_yr3[i] = int(data_yr3[j][3])
				acc_sales_yoy_yr3[i] = float(data_yr3[j][4])
				break
	for j in reversed(range(len(data_yr4))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr4[j][0]) == i+1:
				sales_yr4[i] = int(data_yr4[j][1])
				sales_yoy_yr4[i] = float(data_yr4[j][2])
				acc_sales_yr4[i] = int(data_yr4[j][3])
				acc_sales_yoy_yr4[i] = float(data_yr4[j][4])
				break

	year_series = [thisyear, thisyear-1,  thisyear-2, thisyear-3, thisyear-4]
	month_series = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月",]

	data = json.dumps({"symbol": symbol, "cname": cname, "year_series": year_series, "month_series": month_series,
		"sales_yr0": sales_yr0, "sales_yoy_yr0": sales_yoy_yr0,
		"acc_sales_yr0": acc_sales_yr0, "acc_sales_yoy_yr0": acc_sales_yoy_yr0,
		"sales_yr1": sales_yr1, "sales_yoy_yr1": sales_yoy_yr1,
		"acc_sales_yr1": acc_sales_yr1, "acc_sales_yoy_yr1": acc_sales_yoy_yr1,
		"sales_yr2": sales_yr2, "sales_yoy_yr2": sales_yoy_yr2,
		"acc_sales_yr2": acc_sales_yr2, "acc_sales_yoy_yr2": acc_sales_yoy_yr2,
		"sales_yr3": sales_yr3, "sales_yoy_yr3": sales_yoy_yr3,
		"acc_sales_yr3": acc_sales_yr3, "acc_sales_yoy_yr3": acc_sales_yoy_yr3,
		"sales_yr4": sales_yr4, "sales_yoy_yr4": sales_yoy_yr4,
		"acc_sales_yr4": acc_sales_yr4, "acc_sales_yoy_yr4": acc_sales_yoy_yr4})

	return HttpResponse(data, mimetype='application/json')

# season_effect和sales_overview唯一的差別只有空陣列的地方，一個宣告空字串一個宣告None
def season_effect(request):
	try:
		symbol = request.session['symbol']
	except:
		symbol = '2330'

	# 找出最新營收的年份是哪一年
	if datetime.today().month == 1:
		thisyear = int(datetime.today().year - 1)
	else:
		thisyear = int(datetime.today().year)

	cname = StockID.objects.filter(symbol=symbol).values_list('cname',flat=True)[0]
	monthly_sales = MonthlySales.objects.filter(symbol=symbol)
	# 抓出最近五年的營收/年增率/累積營收/累積營收年增率，並按月份排序
	data_yr0 = monthly_sales.filter(year=thisyear).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	data_yr1 = monthly_sales.filter(year=thisyear-1).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	data_yr2 = monthly_sales.filter(year=thisyear-2).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	data_yr3 = monthly_sales.filter(year=thisyear-3).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	data_yr4 = monthly_sales.filter(year=thisyear-4).order_by('month').values_list('month','sales','sales_yoy','acc_sales','acc_sales_yoy')
	# 宣告空的串列準備填入五年的資料
	sales_yr0 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yr1 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yr2 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yr3 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yr4 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yoy_yr0 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yoy_yr1 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yoy_yr2 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yoy_yr3 = [None,None,None,None,None,None,None,None,None,None,None,None]
	sales_yoy_yr4 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yr0 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yr1 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yr2 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yr3 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yr4 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yoy_yr0 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yoy_yr1 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yoy_yr2 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yoy_yr3 = [None,None,None,None,None,None,None,None,None,None,None,None]
	acc_sales_yoy_yr4 = [None,None,None,None,None,None,None,None,None,None,None,None]

	for j in reversed(range(len(data_yr0))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr0[j][0]) == i+1:
				sales_yr0[i] = int(data_yr0[j][1])
				sales_yoy_yr0[i] = float(data_yr0[j][2])
				acc_sales_yr0[i] = int(data_yr0[j][3])
				acc_sales_yoy_yr0[i] = float(data_yr0[j][4])
				break
	for j in reversed(range(len(data_yr1))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr1[j][0]) == i+1:
				sales_yr1[i] = int(data_yr1[j][1])
				sales_yoy_yr1[i] = float(data_yr1[j][2])
				acc_sales_yr1[i] = int(data_yr1[j][3])
				acc_sales_yoy_yr1[i] = float(data_yr1[j][4])
				break
	for j in reversed(range(len(data_yr2))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr2[j][0]) == i+1:
				sales_yr2[i] = int(data_yr2[j][1])
				sales_yoy_yr2[i] = float(data_yr2[j][2])
				acc_sales_yr2[i] = int(data_yr2[j][3])
				acc_sales_yoy_yr2[i] = float(data_yr2[j][4])
				break
	for j in reversed(range(len(data_yr3))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr3[j][0]) == i+1:
				sales_yr3[i] = int(data_yr3[j][1])
				sales_yoy_yr3[i] = float(data_yr3[j][2])
				acc_sales_yr3[i] = int(data_yr3[j][3])
				acc_sales_yoy_yr3[i] = float(data_yr3[j][4])
				break
	for j in reversed(range(len(data_yr4))):
		for i in range(12):
			# 比對月份，將資料填入正確的月份
			if int(data_yr4[j][0]) == i+1:
				sales_yr4[i] = int(data_yr4[j][1])
				sales_yoy_yr4[i] = float(data_yr4[j][2])
				acc_sales_yr4[i] = int(data_yr4[j][3])
				acc_sales_yoy_yr4[i] = float(data_yr4[j][4])
				break

	year_series = [thisyear, thisyear-1,  thisyear-2, thisyear-3, thisyear-4]
	month_series = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月",]

	data = json.dumps({"symbol": symbol, "cname": cname, "year_series": year_series, "month_series": month_series,
		"sales_yr0": sales_yr0, "sales_yoy_yr0": sales_yoy_yr0,
		"acc_sales_yr0": acc_sales_yr0, "acc_sales_yoy_yr0": acc_sales_yoy_yr0,
		"sales_yr1": sales_yr1, "sales_yoy_yr1": sales_yoy_yr1,
		"acc_sales_yr1": acc_sales_yr1, "acc_sales_yoy_yr1": acc_sales_yoy_yr1,
		"sales_yr2": sales_yr2, "sales_yoy_yr2": sales_yoy_yr2,
		"acc_sales_yr2": acc_sales_yr2, "acc_sales_yoy_yr2": acc_sales_yoy_yr2,
		"sales_yr3": sales_yr3, "sales_yoy_yr3": sales_yoy_yr3,
		"acc_sales_yr3": acc_sales_yr3, "acc_sales_yoy_yr3": acc_sales_yoy_yr3,
		"sales_yr4": sales_yr4, "sales_yoy_yr4": sales_yoy_yr4,
		"acc_sales_yr4": acc_sales_yr4, "acc_sales_yoy_yr4": acc_sales_yoy_yr4})

	return HttpResponse(data, mimetype='application/json')

def price_momentum(request):
	try:
		symbol = request.session['symbol']
	except:
		symbol = '2330'
	cname = list(StockID.objects.filter(symbol=symbol).values_list('cname',flat=True))[0]
	# 將需要使用的欄位從資料庫取出
	monthly_sales = MonthlySales.objects.filter(symbol=symbol).order_by('ID').values_list('ID', 'sales_yoy', 'acc_sales_yoy')
	monthly_stockprice = StockPrice.objects.filter(symbol=symbol).order_by('ID').values_list('ID', 'p_open', 'p_high', 'p_low', 'p_close')
	# 宣告json_data要使用的串列
	stock_date = []
	stock_open = []
	stock_high = []
	stock_low = []
	stock_close = []
	sales_yoy = []
	acc_sales_yoy = []
	for i in range(len(monthly_stockprice)):
		stock_date.append(str(monthly_stockprice[i][0][:6]))
		stock_open.append(float(monthly_stockprice[i][1]))
		stock_high.append(float(monthly_stockprice[i][2]))
		stock_low.append(float(monthly_stockprice[i][3]))
		stock_close.append(float(monthly_stockprice[i][4]))	
		sales_yoy.append(None)
		acc_sales_yoy.append(None)
		# 正常來說，股價資料應該會比營收資料新，所以用股價日期為準，將營收填入對應日期
		for j in reversed(range(len(monthly_sales))):
			if monthly_stockprice[i][0] == monthly_sales[j][0]:
				sales_yoy[i] = float(monthly_sales[j][1])
				acc_sales_yoy[i] = float(monthly_sales[j][2])
				break

	# 只將最近5年的資料傳送給網頁使用
	data = json.dumps({"symbol": symbol, "cname": cname, "stock_date": stock_date[-60:],
		"stock_open": stock_open[-60:], "stock_high": stock_high[-60:],
		"stock_low": stock_low[-60:], "stock_close": stock_close[-60:],
		"sales_yoy": sales_yoy[-60:], "acc_sales_yoy": acc_sales_yoy[-60:]})
	
	return HttpResponse(data, mimetype='application/json')

def basic_overview(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		cname = list(StockID.objects.filter(symbol=symbol).values_list("cname",flat=True))[0]	
		balance_sheet = SeasonBalanceSheet.objects.filter(symbol=symbol).order_by("-year", "-season")
		income_statement = SeasonIncomeStatement.objects.filter(symbol=symbol).order_by("-year", "-season")
		cash_flow = SeasonCashFlow.objects.filter(symbol=symbol).order_by("-year", "-season")
		financial_ratio = SeasonFinancialRatio.objects.filter(symbol=symbol).order_by("-year", "-season")
		# 從各個資料庫中取出該檔股票需要使用的資料
		quarter_name = income_statement.values_list("date",flat=True)
		total_operating_revenue = income_statement.values_list("total_operating_revenue",flat=True)
		total_operating_revenue_yoy = income_statement.values_list("total_operating_revenue_yoy",flat=True)
		accounts_receivable_turnover_ratio = financial_ratio.values_list("accounts_receivable_turnover_ratio",flat=True)
		inventory_turnover_ratio = financial_ratio.values_list("inventory_turnover_ratio",flat=True)
		inventory_sales_ratio = financial_ratio.values_list("inventory_sales_ratio",flat=True)
		available_for_sale_to_equity_ratio = financial_ratio.values_list("available_for_sale_to_equity_ratio",flat=True)
		financial_debt_ratio = financial_ratio.values_list("financial_debt_ratio",flat=True)
		intangible_asset_to_equity_ratio = financial_ratio.values_list("intangible_asset_to_equity_ratio",flat=True)
		total_property_plant_and_equipment = balance_sheet.values_list("total_property_plant_and_equipment",flat=True)
		fixed_asset_turnover_ratio = financial_ratio.values_list("fixed_asset_turnover_ratio",flat=True)
		depreciation_expense = cash_flow.values_list("depreciation_expense",flat=True)
		depreciation_to_sales_ratio = financial_ratio.values_list("depreciation_to_sales_ratio",flat=True)
		gross_profit_margin = financial_ratio.values_list("gross_profit_margin",flat=True)
		operating_profit_margin = financial_ratio.values_list("operating_profit_margin",flat=True)
		earnings_per_share = income_statement.values_list("total_basic_earnings_per_share",flat=True)
		net_operating_income_loss = income_statement.values_list("net_operating_income_loss",flat=True)
		operating_profit_to_net_profit_before_tax_ratio = financial_ratio.values_list("operating_profit_to_net_profit_before_tax_ratio",flat=True)
		net_cash_flows_from_used_in_operating_activities = cash_flow.values_list("net_cash_flows_from_used_in_operating_activities",flat=True)
		net_cash_flows_from_used_in_investing_activities = cash_flow.values_list("net_cash_flows_from_used_in_investing_activities",flat=True)
		free_cash_flow = cash_flow.values_list("free_cash_flow",flat=True)
		tax_rate = financial_ratio.values_list("tax_rate",flat=True)
		ordinary_share = balance_sheet.values_list("ordinary_share",flat=True)
		# 為各個資料數列準備一個空的串列來儲存
		quarter_name_series = []
		total_operating_revenue_series = []
		total_operating_revenue_yoy_series = []
		accounts_receivable_turnover_ratio_series = []
		inventory_turnover_ratio_series = []
		inventory_sales_ratio_series = []
		available_for_sale_to_equity_ratio_series = []
		financial_debt_ratio_series = []
		intangible_asset_to_equity_ratio_series = []
		total_property_plant_and_equipment_series = []
		fixed_asset_turnover_ratio_series = []
		depreciation_expense_series = []
		depreciation_to_sales_ratio_series = []
		gross_profit_margin_series = []
		operating_profit_margin_series = []
		earnings_per_share_series = []
		net_operating_income_loss_series = []
		operating_profit_to_net_profit_before_tax_ratio_series = []
		net_cash_flows_from_used_in_operating_activities_series = []
		net_cash_flows_from_used_in_investing_activities_series = []
		free_cash_flow_series = []
		tax_rate_series = []
		ordinary_share_series = []
		# 如果串列不到20筆資料，就塞入空值，大於的話就只取20筆
		for i in range(20):
			try:
				quarter_name[i]
				total_operating_revenue[i]
				total_operating_revenue_yoy[i]
				accounts_receivable_turnover_ratio[i]
				inventory_turnover_ratio[i]
				inventory_sales_ratio[i]
				available_for_sale_to_equity_ratio[i]
				financial_debt_ratio[i]
				intangible_asset_to_equity_ratio[i]
				total_property_plant_and_equipment[i]
				fixed_asset_turnover_ratio[i]
				depreciation_expense[i]
				depreciation_to_sales_ratio[i]
				gross_profit_margin[i]
				operating_profit_margin[i]
				earnings_per_share[i]
				net_operating_income_loss[i]
				operating_profit_to_net_profit_before_tax_ratio[i]
				net_cash_flows_from_used_in_operating_activities[i]
				net_cash_flows_from_used_in_investing_activities[i]
				free_cash_flow[i]
				tax_rate[i]
				ordinary_share[i]
			except:
				quarter_name_series.append("")
				total_operating_revenue_series.append("")
				total_operating_revenue_yoy_series.append("")
				accounts_receivable_turnover_ratio_series.append("")
				inventory_turnover_ratio_series.append("")
				inventory_sales_ratio_series.append("")
				available_for_sale_to_equity_ratio_series.append("")
				financial_debt_ratio_series.append("")
				intangible_asset_to_equity_ratio_series.append("")
				total_property_plant_and_equipment_series.append("")
				fixed_asset_turnover_ratio_series.append("")
				depreciation_expense_series.append("")
				depreciation_to_sales_ratio_series.append("")
				gross_profit_margin_series.append("")
				operating_profit_margin_series.append("")
				earnings_per_share_series.append("")
				net_operating_income_loss_series.append("")
				operating_profit_to_net_profit_before_tax_ratio_series.append("")
				net_cash_flows_from_used_in_operating_activities_series.append("")
				net_cash_flows_from_used_in_investing_activities_series.append("")
				free_cash_flow_series.append("")
				tax_rate_series.append("")
				ordinary_share_series.append("")
			else:
				quarter_name_series.append(quarter_name[i])
				total_operating_revenue_series.append(int(total_operating_revenue[i]))
				total_operating_revenue_yoy_series.append(float(total_operating_revenue_yoy[i]))
				accounts_receivable_turnover_ratio_series.append(float(accounts_receivable_turnover_ratio[i]))
				inventory_turnover_ratio_series.append(float(inventory_turnover_ratio[i]))
				inventory_sales_ratio_series.append(float(inventory_sales_ratio[i]))
				available_for_sale_to_equity_ratio_series.append(float(available_for_sale_to_equity_ratio[i]))
				financial_debt_ratio_series.append(float(financial_debt_ratio[i]))
				intangible_asset_to_equity_ratio_series.append(float(intangible_asset_to_equity_ratio[i]))
				total_property_plant_and_equipment_series.append(int(total_property_plant_and_equipment[i]))
				fixed_asset_turnover_ratio_series.append(float(fixed_asset_turnover_ratio[i]))
				depreciation_expense_series.append(int(depreciation_expense[i]))
				depreciation_to_sales_ratio_series.append(float(depreciation_to_sales_ratio[i]))
				gross_profit_margin_series.append(float(gross_profit_margin[i]))
				operating_profit_margin_series.append(float(operating_profit_margin[i]))
				earnings_per_share_series.append(float(earnings_per_share[i]))
				net_operating_income_loss_series.append(int(net_operating_income_loss[i]))
				operating_profit_to_net_profit_before_tax_ratio_series.append(float(operating_profit_to_net_profit_before_tax_ratio[i]))
				net_cash_flows_from_used_in_operating_activities_series.append(int(net_cash_flows_from_used_in_operating_activities[i]))
				net_cash_flows_from_used_in_investing_activities_series.append(int(net_cash_flows_from_used_in_investing_activities[i]))
				free_cash_flow_series.append(int(free_cash_flow[i]))
				tax_rate_series.append(float(tax_rate[i]))
				ordinary_share_series.append(float(ordinary_share[i]/10))
				# pdb.set_trace()
		data = json.dumps({"symbol": symbol, "cname": cname,
			"quarter_name": quarter_name_series[::-1],
			"total_operating_revenue": total_operating_revenue_series[::-1],
			"total_operating_revenue_yoy": total_operating_revenue_yoy_series[::-1],
			"accounts_receivable_turnover_ratio": accounts_receivable_turnover_ratio_series[::-1],
			"inventory_turnover_ratio": inventory_turnover_ratio_series[::-1],
			"inventory_sales_ratio": inventory_sales_ratio_series[::-1],
			"available_for_sale_to_equity_ratio": available_for_sale_to_equity_ratio_series[::-1],
			"financial_debt_ratio": financial_debt_ratio_series[::-1],
			"intangible_asset_to_equity_ratio": intangible_asset_to_equity_ratio_series[::-1],
			"total_property_plant_and_equipment": total_property_plant_and_equipment_series[::-1],
			"fixed_asset_turnover_ratio": fixed_asset_turnover_ratio_series[::-1],
			"depreciation_expense": depreciation_expense_series[::-1],
			"depreciation_to_sales_ratio": depreciation_to_sales_ratio_series[::-1],
			"gross_profit_margin": gross_profit_margin_series[::-1],
			"operating_profit_margin": operating_profit_margin_series[::-1],
			"earnings_per_share": earnings_per_share_series[::-1],
			"net_operating_income_loss": net_operating_income_loss_series[::-1],
			"operating_profit_to_net_profit_before_tax_ratio": operating_profit_to_net_profit_before_tax_ratio_series[::-1],
			"net_cash_flows_from_used_in_operating_activities": net_cash_flows_from_used_in_operating_activities_series[::-1],
			"net_cash_flows_from_used_in_investing_activities": net_cash_flows_from_used_in_investing_activities_series[::-1],
			"free_cash_flow": free_cash_flow_series[::-1],
			"tax_rate":tax_rate_series[::-1],
			"ordinary_share": ordinary_share_series[::-1]})
		return HttpResponse(data, mimetype="application/json")

def defensive_indicator(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		income_statement = SeasonIncomeStatement.objects.filter(symbol=symbol).order_by("-year", "-season")
		financial_ratio = SeasonFinancialRatio.objects.filter(symbol=symbol).order_by("-year", "-season")
		# 從各個資料庫中取出該檔股票需要使用的資料
		quarter_name = income_statement.values_list("date",flat=True)
		accounts_receivable_turnover_ratio = financial_ratio.values_list("accounts_receivable_turnover_ratio",flat=True)
		inventory_turnover_ratio = financial_ratio.values_list("inventory_turnover_ratio",flat=True)
		inventory_sales_ratio = financial_ratio.values_list("inventory_sales_ratio",flat=True)
		total_operating_revenue = income_statement.values_list("total_operating_revenue",flat=True)		
		# 為各個資料數列準備一個空的串列來儲存
		quarter_name_series = []
		accounts_receivable_turnover_ratio_series = []
		inventory_turnover_ratio_series = []
		inventory_sales_ratio_series = []
		total_operating_revenue_series = []		
		# 如果串列不到20筆資料，就塞入空值，大於的話就只取20筆
		for i in range(20):
			try:
				quarter_name[i]
				accounts_receivable_turnover_ratio[i]
				inventory_turnover_ratio[i]
				inventory_sales_ratio[i]
				total_operating_revenue[i]
			except:
				quarter_name_series.append("")
				accounts_receivable_turnover_ratio_series.append(0)
				inventory_turnover_ratio_series.append(0)
				inventory_sales_ratio_series.append(0)
				total_operating_revenue_series.append(0)
			else:
				quarter_name_series.append(quarter_name[i])
				accounts_receivable_turnover_ratio_series.append(float(accounts_receivable_turnover_ratio[i]))
				inventory_turnover_ratio_series.append(float(inventory_turnover_ratio[i]))
				inventory_sales_ratio_series.append(float(inventory_sales_ratio[i]))
				total_operating_revenue_series.append(int(total_operating_revenue[i]))
		data = json.dumps({"quarter_name": quarter_name_series[::-1],
			"accounts_receivable_turnover_ratio": accounts_receivable_turnover_ratio_series[::-1],
			"inventory_turnover_ratio": inventory_turnover_ratio_series[::-1],
			"inventory_sales_ratio": inventory_sales_ratio_series[::-1],
			"total_operating_revenue": total_operating_revenue_series[::-1]})
		return HttpResponse(data, mimetype="application/json")

def potentialrisk_indicator(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		income_statement = SeasonIncomeStatement.objects.filter(symbol=symbol).order_by("-year", "-season")
		financial_ratio = SeasonFinancialRatio.objects.filter(symbol=symbol).order_by("-year", "-season")
		# 從各個資料庫中取出該檔股票需要使用的資料
		quarter_name = income_statement.values_list("date",flat=True)
		available_for_sale_to_equity_ratio = financial_ratio.values_list("available_for_sale_to_equity_ratio",flat=True)
		financial_debt_ratio = financial_ratio.values_list("financial_debt_ratio",flat=True)
		intangible_asset_to_equity_ratio = financial_ratio.values_list("intangible_asset_to_equity_ratio",flat=True)
		# 為各個資料數列準備一個空的串列來儲存
		quarter_name_series = []
		available_for_sale_to_equity_ratio_series = []
		financial_debt_ratio_series = []
		intangible_asset_to_equity_ratio_series = []
		# 如果串列不到20筆資料，就塞入空值，大於的話就只取20筆
		for i in range(20):
			try:
				quarter_name[i]
				available_for_sale_to_equity_ratio[i]
				financial_debt_ratio[i]
				intangible_asset_to_equity_ratio[i]
			except:
				quarter_name_series.append("")
				available_for_sale_to_equity_ratio_series.append(0)
				financial_debt_ratio_series.append(0)
				intangible_asset_to_equity_ratio_series.append(0)
			else:
				quarter_name_series.append(quarter_name[i])
				available_for_sale_to_equity_ratio_series.append(float(available_for_sale_to_equity_ratio[i]))
				financial_debt_ratio_series.append(float(financial_debt_ratio[i]))
				intangible_asset_to_equity_ratio_series.append(float(intangible_asset_to_equity_ratio[i]))		
		data = json.dumps({"quarter_name": quarter_name_series[::-1],
			"available_for_sale_to_equity_ratio": available_for_sale_to_equity_ratio_series[::-1],
			"financial_debt_ratio": financial_debt_ratio_series[::-1],
			"intangible_asset_to_equity_ratio": intangible_asset_to_equity_ratio_series[::-1]})
		return HttpResponse(data, mimetype="application/json")

def profitable_indicator_1(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		income_statement = SeasonIncomeStatement.objects.filter(symbol=symbol).order_by("-year", "-season")
		financial_ratio = SeasonFinancialRatio.objects.filter(symbol=symbol).order_by("-year", "-season")
		# 從各個資料庫中取出該檔股票需要使用的資料
		quarter_name = income_statement.values_list("date",flat=True)
		total_operating_revenue_yoy = income_statement.values_list("total_operating_revenue_yoy",flat=True)		
		operating_profit_margin = financial_ratio.values_list("operating_profit_margin",flat=True)
		earnings_per_share = income_statement.values_list("total_basic_earnings_per_share",flat=True)		
		# 為各個資料數列準備一個空的串列來儲存
		quarter_name_series = []
		total_operating_revenue_yoy_series = []		
		operating_profit_margin_series = []
		earnings_per_share_series = []		
		# 如果串列不到20筆資料，就塞入空值，大於的話就只取20筆
		for i in range(20):
			try:
				quarter_name[i]
				total_operating_revenue_yoy[i]
				operating_profit_margin[i]
				earnings_per_share[i]
			except:
				quarter_name_series.append("")
				total_operating_revenue_yoy_series.append(0)
				operating_profit_margin_series.append(0)
				earnings_per_share_series.append(0)
			else:
				quarter_name_series.append(quarter_name[i])
				total_operating_revenue_yoy_series.append(float(total_operating_revenue_yoy[i]))
				operating_profit_margin_series.append(float(operating_profit_margin[i]))
				earnings_per_share_series.append(float(earnings_per_share[i]))
		
		data = json.dumps({"quarter_name": quarter_name_series[::-1],
			"total_operating_revenue_yoy": total_operating_revenue_yoy_series[::-1],			
			"operating_profit_margin": operating_profit_margin_series[::-1],
			"earnings_per_share": earnings_per_share_series[::-1]})
		return HttpResponse(data, mimetype="application/json")

def profitable_indicator_2(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		income_statement = SeasonIncomeStatement.objects.filter(symbol=symbol).order_by("-year", "-season")
		financial_ratio = SeasonFinancialRatio.objects.filter(symbol=symbol).order_by("-year", "-season")
		# 從各個資料庫中取出該檔股票需要使用的資料
		quarter_name = income_statement.values_list("date",flat=True)		
		depreciation_to_sales_ratio = financial_ratio.values_list("depreciation_to_sales_ratio",flat=True)
		gross_profit_margin = financial_ratio.values_list("gross_profit_margin",flat=True)
		operating_profit_margin = financial_ratio.values_list("operating_profit_margin",flat=True)
		earnings_per_share = income_statement.values_list("total_basic_earnings_per_share",flat=True)		
		# 為各個資料數列準備一個空的串列來儲存
		quarter_name_series = []
		depreciation_to_sales_ratio_series = []
		gross_profit_margin_series = []
		operating_profit_margin_series = []
		earnings_per_share_series = []		
		# 如果串列不到20筆資料，就塞入空值，大於的話就只取20筆
		for i in range(20):
			try:
				quarter_name[i]
				depreciation_to_sales_ratio[i]
				gross_profit_margin[i]
				operating_profit_margin[i]
				earnings_per_share[i]
			except:
				quarter_name_series.append("")
				depreciation_to_sales_ratio_series.append(0)
				gross_profit_margin_series.append(0)
				operating_profit_margin_series.append(0)
				earnings_per_share_series.append(0)
			else:
				quarter_name_series.append(quarter_name[i])
				depreciation_to_sales_ratio_series.append(float(depreciation_to_sales_ratio[i]))
				gross_profit_margin_series.append(float(gross_profit_margin[i]))
				operating_profit_margin_series.append(float(operating_profit_margin[i]))
				earnings_per_share_series.append(float(earnings_per_share[i]))
		
		data = json.dumps({"quarter_name": quarter_name_series[::-1],			
			"depreciation_to_sales_ratio": depreciation_to_sales_ratio_series[::-1],
			"gross_profit_margin": gross_profit_margin_series[::-1],
			"operating_profit_margin": operating_profit_margin_series[::-1],
			"earnings_per_share": earnings_per_share_series[::-1]})
		return HttpResponse(data, mimetype="application/json")

def stability_indicator(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		income_statement = SeasonIncomeStatement.objects.filter(symbol=symbol).order_by("-year", "-season")
		financial_ratio = SeasonFinancialRatio.objects.filter(symbol=symbol).order_by("-year", "-season")
		# 從各個資料庫中取出該檔股票需要使用的資料
		quarter_name = income_statement.values_list("date",flat=True)
		earnings_per_share = income_statement.values_list("total_basic_earnings_per_share",flat=True)
		net_operating_income_loss = income_statement.values_list("net_operating_income_loss",flat=True)
		operating_profit_to_net_profit_before_tax_ratio = financial_ratio.values_list("operating_profit_to_net_profit_before_tax_ratio",flat=True)
		# 為各個資料數列準備一個空的串列來儲存
		quarter_name_series = []
		earnings_per_share_series = []
		net_operating_income_loss_series = []
		operating_profit_to_net_profit_before_tax_ratio_series = []
		# 如果串列不到20筆資料，就塞入空值，大於的話就只取20筆
		for i in range(20):
			try:
				quarter_name[i]
				earnings_per_share[i]
				net_operating_income_loss[i]
				operating_profit_to_net_profit_before_tax_ratio[i]
			except:
				quarter_name_series.append("")
				earnings_per_share_series.append(0)
				net_operating_income_loss_series.append(0)
				operating_profit_to_net_profit_before_tax_ratio_series.append(0)
			else:
				quarter_name_series.append(quarter_name[i])
				earnings_per_share_series.append(float(earnings_per_share[i]))
				net_operating_income_loss_series.append(int(net_operating_income_loss[i]))
				operating_profit_to_net_profit_before_tax_ratio_series.append(float(operating_profit_to_net_profit_before_tax_ratio[i]))
		
		data = json.dumps({"quarter_name": quarter_name_series[::-1],			
			"earnings_per_share": earnings_per_share_series[::-1],
			"net_operating_income_loss": net_operating_income_loss_series[::-1],
			"operating_profit_to_net_profit_before_tax_ratio": operating_profit_to_net_profit_before_tax_ratio_series[::-1]})
		return HttpResponse(data, mimetype="application/json")

def cashflow_indicator(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		income_statement = SeasonIncomeStatement.objects.filter(symbol=symbol).order_by("-year", "-season")
		cash_flow = SeasonCashFlow.objects.filter(symbol=symbol).order_by("-year", "-season")
		# 從各個資料庫中取出該檔股票需要使用的資料
		quarter_name = income_statement.values_list("date",flat=True)		
		net_operating_income_loss = income_statement.values_list("net_operating_income_loss",flat=True)		
		net_cash_flows_from_used_in_operating_activities = cash_flow.values_list("net_cash_flows_from_used_in_operating_activities",flat=True)
		free_cash_flow = cash_flow.values_list("free_cash_flow",flat=True)		
		# 為各個資料數列準備一個空的串列來儲存
		quarter_name_series = []		
		net_operating_income_loss_series = []		
		net_cash_flows_from_used_in_operating_activities_series = []		
		free_cash_flow_series = []		
		# 如果串列不到20筆資料，就塞入空值，大於的話就只取20筆
		for i in range(20):
			try:
				quarter_name[i]
				net_operating_income_loss[i]
				net_cash_flows_from_used_in_operating_activities[i]
				free_cash_flow[i]
			except:
				quarter_name_series.append("")
				net_operating_income_loss_series.append(0)
				net_cash_flows_from_used_in_operating_activities_series.append(0)
				free_cash_flow_series.append(0)
			else:
				quarter_name_series.append(quarter_name[i])
				net_operating_income_loss_series.append(int(net_operating_income_loss[i]))
				net_cash_flows_from_used_in_operating_activities_series.append(int(net_cash_flows_from_used_in_operating_activities[i]))
				free_cash_flow_series.append(int(free_cash_flow[i]))

		data = json.dumps({"quarter_name": quarter_name_series[::-1],			
			"net_operating_income_loss": net_operating_income_loss_series[::-1],
			"net_cash_flows_from_used_in_operating_activities": net_cash_flows_from_used_in_operating_activities_series[::-1],
			"free_cash_flow": free_cash_flow_series[::-1]})
		return HttpResponse(data, mimetype="application/json")

def bigchip_tracking(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		cname = StockID.objects.filter(symbol=symbol).values_list("cname",flat=True)[0]
		# 將需要使用的欄位從資料庫取出
		stock_price = StockPrice.objects.filter(symbol=symbol).order_by('ID').values_list('ID', 'p_open', 'p_high', 'p_low', 'p_close')
		chip_dist = ChipDistridution.objects.filter(symbol=symbol).order_by('ID').values_list('ID',
			'bigchip_holders', 'bigchip_holdings', 'bigchip_percent', 'bigchip_monthly_change',
			'bigchip_holders_2nd', 'bigchip_holdings_2nd', 'bigchip_percent_2nd',
			'bigchip_holders_3rd', 'bigchip_holdings_3rd', 'bigchip_percent_3rd')
		# 宣告json_data要使用的串列
		stock_date = []
		stock_open = []
		stock_high = []
		stock_low = []
		stock_close = []
		bigchip_holders = []
		bigchip_holdings = []
		bigchip_percent = []
		bigchip_monthly_change = []
		bigchip_holders_2nd = []
		bigchip_holdings_2nd = []
		bigchip_percent_2nd = []
		bigchip_holders_3rd = []
		bigchip_holdings_3rd = []
		bigchip_percent_3rd = []
		for i in range(len(stock_price)):
			stock_date.append(str(stock_price[i][0][:6]))
			stock_open.append(float(stock_price[i][1]))
			stock_high.append(float(stock_price[i][2]))
			stock_low.append(float(stock_price[i][3]))
			stock_close.append(float(stock_price[i][4]))
			bigchip_holders.append("")
			bigchip_holdings.append("")
			bigchip_percent.append("")
			bigchip_monthly_change.append("")
			bigchip_holders_2nd.append("")
			bigchip_holdings_2nd.append("")
			bigchip_percent_2nd.append("")
			bigchip_holders_3rd.append("")
			bigchip_holdings_3rd.append("")
			bigchip_percent_3rd.append("")
			# 正常來說，股價資料應該會比籌碼資料新，所以用股價日期為準，將籌碼填入對應日期
			for j in reversed(range(len(chip_dist))):
				if stock_price[i][0] == chip_dist[j][0]:
					bigchip_holders[i] = int(chip_dist[j][1])
					bigchip_holdings[i] = int(chip_dist[j][2]/1000)
					bigchip_percent[i] = float(chip_dist[j][3])
					bigchip_monthly_change[i] = int(chip_dist[j][4]/1000)
					if chip_dist[j][5] != None:
						bigchip_holders_2nd[i] = int(chip_dist[j][5])
						bigchip_holdings_2nd[i] = int(chip_dist[j][6]/1000)
						bigchip_percent_2nd[i] = float(chip_dist[j][7])
						bigchip_holders_3rd[i] = int(chip_dist[j][8])
						bigchip_holdings_3rd[i] = int(chip_dist[j][9]/1000)
						bigchip_percent_3rd[i] = float(chip_dist[j][10])
					break

		# 只將最近5年的資料傳送給網頁使用
		data = json.dumps({"symbol": symbol, "cname": cname,
			"stock_date": stock_date[-60:],
			"stock_open": stock_open[-60:],
			"stock_high": stock_high[-60:],
			"stock_low": stock_low[-60:],
			"stock_close": stock_close[-60:],
			"bigchip_holders": bigchip_holders[-60:],
			"bigchip_holdings": bigchip_holdings[-60:],
			"bigchip_percent": bigchip_percent[-60:],
			"bigchip_monthly_change": bigchip_monthly_change[-60:],
			"bigchip_holders_2nd": bigchip_holders_2nd[-60:],
			"bigchip_holdings_2nd": bigchip_holdings_2nd[-60:],
			"bigchip_percent_2nd": bigchip_percent_2nd[-60:],
			"bigchip_holders_3rd": bigchip_holders_3rd[-60:],
			"bigchip_holdings_3rd": bigchip_holdings_3rd[-60:],
			"bigchip_percent_3rd": bigchip_percent_3rd[-60:]})

		return HttpResponse(data, mimetype="application/json")

# bigchip_tracking和bigchip_tracking_chart唯一的差別只有空陣列的地方，一個宣告空字串一個宣告None
def bigchip_tracking_chart(request):
	try:
		symbol = request.session["symbol"]
	except:
		symbol = "2330"
	else:
		cname = StockID.objects.filter(symbol=symbol).values_list("cname",flat=True)[0]
		# 將需要使用的欄位從資料庫取出
		stock_price = StockPrice.objects.filter(symbol=symbol).order_by('ID').values_list('ID', 'p_open', 'p_high', 'p_low', 'p_close')
		chip_dist = ChipDistridution.objects.filter(symbol=symbol).order_by('ID').values_list('ID',
			'bigchip_holders', 'bigchip_holdings', 'bigchip_percent', 'bigchip_monthly_change')
		# 宣告json_data要使用的串列
		stock_date = []
		stock_open = []
		stock_high = []
		stock_low = []
		stock_close = []
		bigchip_holders = []
		bigchip_holdings = []
		bigchip_percent = []
		bigchip_monthly_change = []
		for i in range(len(stock_price)):
			stock_date.append(str(stock_price[i][0][:6]))
			stock_open.append(float(stock_price[i][1]))
			stock_high.append(float(stock_price[i][2]))
			stock_low.append(float(stock_price[i][3]))
			stock_close.append(float(stock_price[i][4]))
			bigchip_holders.append(None)
			bigchip_holdings.append(None)
			bigchip_percent.append(None)
			bigchip_monthly_change.append(None)
			# 正常來說，股價資料應該會比籌碼資料新，所以用股價日期為準，將籌碼填入對應日期
			for j in reversed(range(len(chip_dist))):
				if stock_price[i][0] == chip_dist[j][0]:
					bigchip_holders[i] = int(chip_dist[j][1])
					bigchip_holdings[i] = int(chip_dist[j][2]/1000)
					bigchip_percent[i] = float(chip_dist[j][3])
					bigchip_monthly_change[i] = int(chip_dist[j][4]/1000)
					break

		# 只將最近5年的資料傳送給網頁使用
		data = json.dumps({"symbol": symbol, "cname": cname,
			"stock_date": stock_date[-60:],
			"stock_open": stock_open[-60:],
			"stock_high": stock_high[-60:],
			"stock_low": stock_low[-60:],
			"stock_close": stock_close[-60:],
			"bigchip_holders": bigchip_holders[-60:],
			"bigchip_holdings": bigchip_holdings[-60:],
			"bigchip_percent": bigchip_percent[-60:],
			"bigchip_monthly_change": bigchip_monthly_change[-60:]})

		return HttpResponse(data, mimetype="application/json")




def sales_momentum_old(request):
	try:
		symbol = request.session['symbol']
	except:
		symbol = '2330'
	cname = list(StockID.objects.filter(symbol=symbol).values_list('cname',flat=True))[0]
	salesyoy = list(MonthlySales.objects.filter(symbol=symbol).order_by('year','month').values_list('sales_yoy',flat=True))
	accsalesyoy = list(MonthlySales.objects.filter(symbol=symbol).order_by('year','month').values_list('acc_sales_yoy',flat=True))
	sales = list(MonthlySales.objects.filter(symbol=symbol).order_by('year','month').values_list('sales',flat=True))
	#計算全部的資料筆數
	dataNum_salesyoy = len(salesyoy)
	dataNum_show = 36
	#將資料轉為float及int格式存到list
	salesyoy_series = []
	accsalesyoy_series = []
	sales_series = []
	xAxis_cat_series = []

	if dataNum_salesyoy < dataNum_show:
		dataNum_show = dataNum_salesyoy
	
	for syoy in salesyoy[-dataNum_show:]:
		if syoy is not None:
			salesyoy_series.append(float(syoy))
		else:
			salesyoy_series.append(0)
	for accs in accsalesyoy[-dataNum_show:]:
		if accs is not None:
			accsalesyoy_series.append(float(accs))
		else:
			accsalesyoy_series.append(0)
	for s in sales[-dataNum_show:]:
		if s is not None:
			sales_series.append(int(s))
		else:
			sales_series.append(0)
	xAxis_cat = list(MonthlySales.objects.filter(symbol=symbol).order_by('year','month').values_list('ID'))
	for x in xAxis_cat[-dataNum_show:]:
		if x is not None:
			if (str(x)[7:9] == '01') | (str(x)[7:9] == '04') | (str(x)[7:9] == '07') | (str(x)[7:9] == '10'):
				xAxis_cat_series.append(str(x)[3:9])
			else:
				xAxis_cat_series.append(str(x)[7:9])
		else:
			xAxis_cat_series.append('')

	data = json.dumps({"symbol": symbol, "cname": cname, "xAxis_cat_series": xAxis_cat_series, "salesyoy_series": salesyoy_series, "accsalesyoy_series": accsalesyoy_series, "sales_series": sales_series})
	return HttpResponse(data, mimetype='application/json')