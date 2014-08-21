#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Sum, Avg, Max, Min
from datetime import date, datetime
import urllib, urllib2
from urllib2 import URLError
from bs4 import BeautifulSoup
import json
import operator
from decimal import Decimal

import pdb
from stockid.models import StockID
from stockprice.models import StockPrice, LatestStockPrice
from stocksales.models import MonthlySales
from stockfins.models import SeasonBalanceSheet, SeasonIncomeStatement, SeasonCashFlow, SeasonFinancialRatio
from stockfins.models import AnnualIncomeStatement, AnnualCashFlow, AnnualFinancialRatio, EarningsPayout
from stockchip.models import ChipDistridution
from economics.models import TaiwanEconomicsIndicator

def pickstock_home(request):
	return render_to_response("pickstock_home.html")

def string_to_decimal(data):
	return(Decimal(data.strip().replace(',', '')))

def pickstock_bluechip(request):
	# =========================
	#  第I部分：篩選股票的條件
	# =========================
		# 條件參數：月
	mth_streak = int(request.GET["mth_streak"])
	salesYoY_mth_level = float(request.GET["salesYoY_mth_level"])
	optimistic_level = 1
	conservative_level = 0.8
	# 條件參數：季
	qtr_streak = int(request.GET["qtr_streak"])
	opm_qtr_level = float(request.GET["opm_qtr_level"])
	eps_qtr_level = float(request.GET["eps_qtr_level"])
	cf_qtr_level = int(request.GET["cf_qtr_level"])
	fdebt_qtr_level = float(request.GET["fdebt_qtr_level"])
	# # 條件參數：年（尚未啟用）
	# yr_streak = int(request.GET["yr_streak"])
	# eps_yr_condition = [0, 4]
	# cf_yr_condition = [0, 4]
	# opm_yr_condition = [20, 4]
	# payout_yr_condition = [50, 4]

	# =========================
	#  第II部分：開始根據條件篩選
	# =========================
	stocks = StockID.objects.all()
	seasonBS = SeasonBalanceSheet.objects.all()
	seasonIS = SeasonIncomeStatement.objects.all()
	seasonCF = SeasonCashFlow.objects.all()
	seasonFR = SeasonFinancialRatio.objects.all()
	monthSales = MonthlySales.objects.all()	
	dailyPrice =LatestStockPrice.objects.all()
	annualDVD = EarningsPayout.objects.all()
	annualFR = AnnualFinancialRatio.objects.all()

	result_list = []
	for stock in stocks:
		result_list.append(stock.symbol)

	# ---------------
	#  季條件篩選
	# ---------------
	if qtr_streak != 0:
		# 營益率
		temp_list = []
		for stock in result_list:
			if seasonFR.filter(symbol=stock):
				opm_qtr = seasonFR.filter(symbol=stock).order_by("-ID")[:qtr_streak].values_list("operating_profit_margin", flat=True)
				if reduce(lambda x,y: x and (y >= opm_qtr_level), opm_qtr, True):
					temp_list.append(stock)
		result_list = list(set.intersection(set(temp_list),set(result_list)))
		# EPS
		temp_list = []
		for stock in result_list:
			if seasonIS.filter(symbol=stock):
				eps_qtr = seasonIS.filter(symbol=stock).order_by("-ID")[:qtr_streak].values_list("total_basic_earnings_per_share", flat=True)
				if reduce(lambda x,y: x and (y >= eps_qtr_level), eps_qtr, True):
					temp_list.append(stock)
		result_list = list(set.intersection(set(temp_list),set(result_list)))
		# 條件：自由現金流量
		temp_list = []
		for stock in result_list:
			if seasonCF.filter(symbol=stock):
				cf_qtr = seasonCF.filter(symbol=stock).order_by("-ID")[:qtr_streak].values_list("free_cash_flow", flat=True)
				if sum(filter(None, cf_qtr)) >= cf_qtr_level:
					temp_list.append(stock)
		result_list = list(set.intersection(set(temp_list),set(result_list)))
		# 條件：金融負債比率
		temp_list = []
		for stock in result_list:
			if seasonFR.filter(symbol=stock):
				fdebt_qtr = seasonFR.filter(symbol=stock).order_by("-ID")[:qtr_streak].values_list("financial_debt_ratio", flat=True)
				if reduce(lambda x,y: x and (y <= fdebt_qtr_level), fdebt_qtr, True):
					temp_list.append(stock)
		result_list = list(set.intersection(set(temp_list),set(result_list)))
	# -------------
	#  月條件篩選
	# -------------
	if mth_streak != 0:
		# 營收年增率
		temp_list = []
		for stock in result_list:
			if monthSales.filter(symbol=stock):
				salesYoY_mth = monthSales.filter(symbol=stock).order_by("-ID")[:mth_streak].values_list("sales_yoy", flat=True)
				if reduce(lambda x,y: x and (y >= salesYoY_mth_level), salesYoY_mth, True):
					temp_list.append(stock)
		result_list = list(set.intersection(set(temp_list),set(result_list)))

	result_list = sorted(result_list)

	# ============================
	#  第III部分：取出潛力股的各項資料
	# ============================
	pickstock_id = []
	pickstock_cname = []
	pickstock_opm = []
	pickstock_eps = []
	pickstock_freecf_sum = []
	pickstock_salesyoy = []
	pickstock_forcast_yr_eps = []
	pickstock_forcast_yr_eps_conservative = []
	pickstock_dailyprice = []
	pickstock_forward_per = []
	pickstock_forward_per_conservative = []
	pickstock_dividends = []
	pickstock_payoutratio = []
	pickstock_forcast_dividends = []
	pickstock_forcast_yield = []

	for stock in result_list:
		pickstock_BS = seasonBS.filter(symbol=stock).order_by("-ID")
		pickstock_IS = seasonIS.filter(symbol=stock).order_by("-ID")
		pickstock_CF = seasonCF.filter(symbol=stock).order_by("-ID")
		pickstock_FR = seasonFR.filter(symbol=stock).order_by("-ID")
		pickstock_MS = monthSales.filter(symbol=stock).order_by("-ID")
		pickstock_DVD =  annualDVD.filter(symbol=stock).order_by("-ID")
		pickstock_yFR = annualFR.filter(symbol=stock).order_by("-ID")
		# ------------------------------------------------------------
		# 取出最近4季的營益率、EPS、加總後自由現金流、以及最近3個月的營收年增率
		# ------------------------------------------------------------
		latest_4qtr_qtrname = map(str, pickstock_IS.values_list("ID", flat=True)[:4])[::-1]
		latest_4qtr_opm = map(float, pickstock_FR.values_list("operating_profit_margin", flat=True)[:4])[::-1]
		latest_4qtr_eps = map(float, pickstock_IS.values_list("total_basic_earnings_per_share", flat=True)[:4])[::-1]
		latest_4qtr_freecf_sum = int(sum(pickstock_CF.values_list("free_cash_flow", flat=True)[:4]))
		latest_3mth_mthname = map(str, pickstock_MS.values_list("ID", flat=True)[:3])[::-1]
		latest_3mth_salesyoy = map(float, pickstock_MS.values_list("sales_yoy", flat=True)[:3])[::-1]
		# --------------------------------------------------------------------------------------
		# 取出最新單月累積營收年增率，最近4季的營收、平均營益率、平均稅率，還有最新的普通股股本(單位:股)、
		# 最新收盤價、最近1年現金股利、配息率
		# --------------------------------------------------------------------------------------
		latest_1mth_acc_salesyoy = float(pickstock_MS.values_list("acc_sales_yoy", flat=True)[0])
		latest_4qtr_sales = map(int, pickstock_IS.values_list("total_operating_revenue", flat=True)[:4])[::-1]
		# 遇到沒有營益率的就跳過該檔股票(通常是金融股)
		if len(latest_4qtr_opm) == 0:
			print(stock)
			continue
		else:
			latest_4qtr_opm_avg = sum(latest_4qtr_opm) / len(latest_4qtr_opm)
		latest_4qtr_taxrate = map(float, pickstock_FR.values_list("tax_rate", flat=True)[:4])[::-1]
		latest_4qtr_taxrate_avg = sum(latest_4qtr_taxrate) / len(latest_4qtr_taxrate)
		latest_1qtr_shares = int(pickstock_BS.values_list("ordinary_share", flat=True)[0]*100)
		if dailyPrice.filter(symbol=stock):
			pickstock_DP = dailyPrice.filter(symbol=stock)
			latest_closeprice = float(pickstock_DP.values_list("p_close", flat=True)[0])
		else:
			latest_closeprice = 0
		if pickstock_DVD:
			latest_1yr_dividends = float(pickstock_DVD.values_list("cash_dividends_all", flat=True)[0])
			latest_1yr_payoutratio = float(pickstock_yFR.values_list("payout_ratio", flat=True)[0]/100)
		else:
			latest_1yr_dividends = 0
			latest_1yr_payoutratio = 0
		# ---------------------------------------------------
		# 若年報未公佈，就估算當年EPS；若年報已公佈，則估算隔年的EPS
		# ---------------------------------------------------
		announced_yr = pickstock_IS.values_list("year",flat=True)[0]
		announced_yr_qtrNo = len(pickstock_IS.filter(year=announced_yr))
		if announced_yr_qtrNo < 4:
			forcast_yr = announced_yr
			announced_qtr_eps = sum(latest_4qtr_eps[(4-announced_yr_qtrNo):])
			# 樂觀預估(營收年增率會加成)
			forcast_qtr_sales = sum(latest_4qtr_sales[:(4-announced_yr_qtrNo)])*(1+latest_1mth_acc_salesyoy*optimistic_level/100)*1000
			forcast_qtr_revenue = forcast_qtr_sales*(latest_4qtr_opm_avg/100)*(1-latest_4qtr_taxrate_avg/100)
			forcast_qtr_eps = forcast_qtr_revenue / latest_1qtr_shares
			forcast_yr_eps = announced_qtr_eps + forcast_qtr_eps
			forward_per = latest_closeprice / forcast_yr_eps
			# 保守預估(營收年增率會打折)
			forcast_qtr_sales_conservative = sum(latest_4qtr_sales[:(4-announced_yr_qtrNo)])*(1+latest_1mth_acc_salesyoy*conservative_level/100)*1000
			forcast_qtr_revenue_conservative = forcast_qtr_sales_conservative*(latest_4qtr_opm_avg/100)*(1-latest_4qtr_taxrate_avg/100)
			forcast_qtr_eps_conservative = forcast_qtr_revenue_conservative / latest_1qtr_shares
			forcast_yr_eps_conservative = announced_qtr_eps + forcast_qtr_eps_conservative
			forward_per_conservative = latest_closeprice / forcast_yr_eps_conservative
		else:
			forcast_yr = announced_yr + 1
			# 樂觀預估
			forcast_qtr_sales = sum(latest_4qtr_sales)*(1+latest_1mth_acc_salesyoy/100)*1000
			forcast_qtr_revenue = forcast_qtr_sales*(latest_4qtr_opm_avg/100)*(1-latest_4qtr_taxrate_avg/100)
			forcast_qtr_eps = forcast_qtr_revenue / latest_1qtr_shares
			forcast_yr_eps = forcast_qtr_eps
			forward_per = latest_closeprice / forcast_yr_eps
			# 保守預估(營收年增率會打折)
			forcast_qtr_sales_conservative = sum(latest_4qtr_sales)*(1+latest_1mth_acc_salesyoy*conservative_level/100)*1000
			forcast_qtr_revenue_conservative = forcast_qtr_sales_conservative*(latest_4qtr_opm_avg/100)*(1-latest_4qtr_taxrate_avg/100)
			forcast_qtr_eps_conservative = forcast_qtr_revenue_conservative / latest_1qtr_shares
			forcast_yr_eps_conservative = forcast_qtr_eps_conservative
			forward_per_conservative = latest_closeprice / forcast_yr_eps_conservative
		# 預估現金股利，EPS用樂觀值和保守值的平均
		forcast_dividends = (forcast_yr_eps+forcast_yr_eps_conservative)/2*latest_1yr_payoutratio
		if latest_closeprice > 0:
			forcast_yield = forcast_dividends / latest_closeprice * 100
		else:
			forcast_yield = 0
		
		pickstock_id.append(stock)
		pickstock_cname.append(StockID.objects.filter(symbol=stock).values_list("cname",flat=True)[0])
		pickstock_opm.append(latest_4qtr_opm)
		pickstock_eps.append(latest_4qtr_eps)
		pickstock_freecf_sum.append(latest_4qtr_freecf_sum)
		pickstock_salesyoy.append(latest_3mth_salesyoy)
		pickstock_forcast_yr_eps.append(forcast_yr_eps)
		pickstock_forcast_yr_eps_conservative.append(forcast_yr_eps_conservative)
		pickstock_dailyprice.append(latest_closeprice)
		pickstock_forward_per.append(forward_per)
		pickstock_forward_per_conservative.append(forward_per_conservative)
		pickstock_dividends.append(latest_1yr_dividends)
		pickstock_payoutratio.append(latest_1yr_payoutratio)
		pickstock_forcast_dividends.append(forcast_dividends)
		pickstock_forcast_yield.append(forcast_yield)

	# --------------------------------------------------------
	# 處理網頁表格標題列的「季度名稱(4季)」、「月份名稱(3個月)」
	# --------------------------------------------------------
	pickstock_qtrname = []
	pickstock_mthname = []
	for qtrname in latest_4qtr_qtrname:
		pickstock_qtrname.append(str(qtrname)[:6])
	for mthname in latest_3mth_mthname:
		pickstock_mthname.append(str(mthname)[:6])

	# ================================
	#  第IV部分：將資料以json格式傳給網頁
	# ================================
	data = json.dumps({"pickstock_id": pickstock_id, "pickstock_cname": pickstock_cname,
		"pickstock_qtrname": pickstock_qtrname,
		"pickstock_opm": pickstock_opm,
		"pickstock_eps": pickstock_eps,
		"pickstock_freecf_sum": pickstock_freecf_sum,
		"pickstock_mthname": pickstock_mthname,
		"pickstock_salesyoy": pickstock_salesyoy,
		"forcast_yr":forcast_yr,
		"pickstock_forcast_yr_eps":pickstock_forcast_yr_eps,
		"pickstock_forcast_yr_eps_conservative":pickstock_forcast_yr_eps_conservative,
		"pickstock_dailyprice": pickstock_dailyprice,
		"pickstock_forward_per": pickstock_forward_per,
		"pickstock_forward_per_conservative": pickstock_forward_per_conservative,
		"pickstock_dividends": pickstock_dividends,
		"pickstock_payoutratio": pickstock_payoutratio,
		"pickstock_forcast_dividends": pickstock_forcast_dividends,
		"pickstock_forcast_yield": pickstock_forcast_yield})

	return HttpResponse(data, mimetype="application/json")