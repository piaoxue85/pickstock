#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
import urllib, urllib2
from urllib2 import URLError
import json
import pdb
from economics.models import TaiwanEconomicsIndicator

# ==============================
#  *** 台灣總體經濟指標追蹤 ***
# ==============================
def tw_economics_home(request):
	return render_to_response('tw_economics.html')

def tw_economics(request):
	tw_economics = TaiwanEconomicsIndicator.objects.all().order_by("date")
	# 從資料庫取出要使用的資料
	twse_date = tw_economics.values_list("date",flat=True)
	twse_open = tw_economics.values_list("twse_open",flat=True)
	twse_high = tw_economics.values_list("twse_high",flat=True)
	twse_low = tw_economics.values_list("twse_low",flat=True)
	twse_close = tw_economics.values_list("twse_close",flat=True)
	twse_pbr = tw_economics.values_list("twse_pbr",flat=True)
	monitoring_indicator = tw_economics.values_list("monitoring_indicator",flat=True)
	composite_leading_index = tw_economics.values_list("composite_leading_index",flat=True)
	composite_leading_index_yoy = tw_economics.values_list("composite_leading_index_yoy",flat=True)
	monetary_aggregates_M1B = tw_economics.values_list("monetary_aggregates_M1B",flat=True)
	monetary_aggregates_M1B_yoy = tw_economics.values_list("monetary_aggregates_M1B_yoy",flat=True)
	# 為各個資料數列準備一個空的串列來儲存
	twse_date_series = []
	twse_open_series = []
	twse_high_series = []
	twse_low_series = []
	twse_close_series = []
	twse_pbr_series = []
	twse_pbr10_series = []
	twse_pbr13_series = []
	twse_pbr16_series = []
	twse_pbr19_series = []
	twse_pbr22_series = []
	monitoring_indicator_series = []
	composite_leading_index_series = []
	composite_leading_index_yoy_series = []
	monetary_aggregates_M1B_series = []
	monetary_aggregates_M1B_yoy_series = []
	# 如果指數的資料更新的太慢，導致已經先有PBR或景氣指標數據而沒有指數時，就先用前期的行情代替
	num_of_data = len(twse_date)
	for i in range(num_of_data):
		if twse_date[i] != None:
			twse_date_series.append(str(twse_date[i]))
			if twse_open[i] != None:
				twse_open_series.append(float(twse_open[i]))
			else:
				twse_open_series.append(float(twse_open_series[i-1]))

			if twse_high[i] != None:
				twse_high_series.append(float(twse_high[i]))
			else:
				twse_high_series.append(float(twse_high_series[i-1]))

			if twse_low[i] != None:
				twse_low_series.append(float(twse_low[i]))
			else:
				twse_low_series.append(float(twse_low_series[i-1]))

			if twse_close[i] != None:
				twse_close_series.append(float(twse_close[i]))
			else:
				twse_close_series.append(float(twse_close_series[i-1]))

			if twse_pbr[i] != None:
				twse_pbr_series.append(float(twse_pbr[i]))
				if twse_close[i] != None:
					twse_pbr10_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 1.0))
					twse_pbr13_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 1.3))
					twse_pbr16_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 1.6))
					twse_pbr19_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 1.9))
					twse_pbr22_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 2.2))
			else:
				# 新方法：PBR尚未公佈的最新數據，用前期數字推算(即假設全體上市公司獲利維持)
				if twse_close[i] != None:
					twse_pbr_series.append(float(twse_pbr_series[i-1] * twse_close_series[i] / twse_close_series[i-1]))
					twse_pbr10_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 1.0))
					twse_pbr13_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 1.3))
					twse_pbr16_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 1.6))
					twse_pbr19_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 1.9))
					twse_pbr22_series.append(int(twse_close_series[i] / twse_pbr_series[i] * 2.2))
				# 舊方法：PBR尚未公佈的最新數據，用前期數字代替
				# twse_pbr_series.append(float(twse_pbr_series[i-1]))
				# if twse_close[i] != None:
				# 	twse_pbr10_series.append(int(twse_close_series[i] / twse_pbr_series[i-1] * 1.0))
				# 	twse_pbr13_series.append(int(twse_close_series[i] / twse_pbr_series[i-1] * 1.3))
				# 	twse_pbr16_series.append(int(twse_close_series[i] / twse_pbr_series[i-1] * 1.6))
				# 	twse_pbr19_series.append(int(twse_close_series[i] / twse_pbr_series[i-1] * 1.9))
				# 	twse_pbr22_series.append(int(twse_close_series[i] / twse_pbr_series[i-1] * 2.2))
				
			# 台灣景氣指標尚未公佈的最新數據以前期的資料填補
			if monitoring_indicator[i] != None:
				monitoring_indicator_series.append(int(monitoring_indicator[i]))
			else:
				monitoring_indicator_series.append(int(monitoring_indicator_series[i-1]))

			if composite_leading_index[i] != None:
				composite_leading_index_series.append(float(composite_leading_index[i]))
			else:
				composite_leading_index_series.append(float(composite_leading_index_series[i-1]))

			if composite_leading_index_yoy[i] != None:
				composite_leading_index_yoy_series.append(float(composite_leading_index_yoy[i]))
			else:
				composite_leading_index_yoy_series.append(float(composite_leading_index_yoy_series[i-1]))

			if monetary_aggregates_M1B[i] != None:
				monetary_aggregates_M1B_series.append(int(monetary_aggregates_M1B[i]))
			else:
				monetary_aggregates_M1B_series.append(int(monetary_aggregates_M1B_series[i-1]))

			if monetary_aggregates_M1B_yoy[i] != None:
				monetary_aggregates_M1B_yoy_series.append(float(monetary_aggregates_M1B_yoy[i]))
			else:
				monetary_aggregates_M1B_yoy_series.append(float(monetary_aggregates_M1B_yoy_series[i-1]))

	# 只將最近10年的資料傳送給網頁使用
	data = json.dumps({"twse_date": twse_date_series[-120:],
			"twse_open": twse_open_series[-120:],
			"twse_high": twse_high_series[-120:],
			"twse_low": twse_low_series[-120:],
			"twse_close": twse_close_series[-120:],
			"twse_pbr": twse_pbr_series[-120:],
			"twse_pbr10": twse_pbr10_series[-120:],
			"twse_pbr13": twse_pbr13_series[-120:],
			"twse_pbr16": twse_pbr16_series[-120:],
			"twse_pbr19": twse_pbr19_series[-120:],
			"twse_pbr22": twse_pbr22_series[-120:],
			"monitoring_indicator": monitoring_indicator_series[-120:],
			"composite_leading_index": composite_leading_index_series[-120:],
			"composite_leading_index_yoy": composite_leading_index_yoy_series[-120:],
			"monetary_aggregates_M1B": monetary_aggregates_M1B_series[-120:],
			"monetary_aggregates_M1B_yoy": monetary_aggregates_M1B_yoy_series[-120:]})

	return HttpResponse(data, mimetype="application/json")

# ==============================
#  *** 美國總體經濟指標追蹤 ***
# ==============================
# FRED官方api網站：https://api.stlouisfed.org/docs/fred/
api_key = "c40cdd5c0ad1ceb7fcf46c8a7cbfaa8e"

def usa_economics_home(request):
	return render_to_response('usa_economics.html')

# ==============================
#  *** 分頁1:GDP佔比分析 ***
# ==============================
observation_start_gdp = "2000-01-01"
# -----------------------
#  *** 實質GDP成長率 ***
# -----------------------
def usa_economics_real_gdp_contribution(request):
	series_id = "GDPC96"
	units = "pca"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------
#  *** 實質GDP/民間消費 ***
# --------------------------
def usa_economics_real_pce_contribution(request):
	series_id = "DPCERY2Q224SBEA"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ---------------------------------
#  *** 實質GDP/民間消費/耐久財 ***
# ---------------------------------
def usa_economics_real_pcdg_contribution(request):
	series_id = "DDURRY2Q224SBEA"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------
#  *** 實質GDP/民間投資 ***
# --------------------------
def usa_economics_real_gpdi_contribution(request):
	series_id = "A006RY2Q224SBEA"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()
		
	return HttpResponse(data, mimetype="application/json")
# -----------------------------------
#  *** 實質GDP/民間投資/住宅投資 ***
# -----------------------------------
def usa_economics_real_prfi_contribution(request):
	series_id = "A011RY2Q224SBEA"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# -------------------------------------
#  *** 實質GDP/民間投資/非住宅投資 ***
# -------------------------------------
def usa_economics_real_pnfi_contribution(request):
	series_id = "A008RY2Q224SBEA"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------
#  *** 實質GDP/進口 ***
# --------------------------
def usa_economics_real_impgs_contribution(request):
	series_id = "A021RY2Q224SBEA"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------
#  *** 實質GDP/出口 ***
# --------------------------
def usa_economics_real_expgs_contribution(request):
	series_id = "A020RY2Q224SBEA"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------------
#  *** 實質GDP/政府支出與投資 ***
# --------------------------------
def usa_economics_real_gce_contribution(request):
	series_id = "A822RY2Q224SBEA"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")

# ==============================
#  *** 分頁1:（續） ***
# ==============================
# -----------------------------
#  *** 實質GDP金額(10億美元) ***
# -----------------------------
def usa_economics_real_gdp_amount(request):
	series_id = "GDPC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ------------------------------------
#  *** 實質GDP/民間消費金額(10億美元) ***
# ------------------------------------
def usa_economics_real_pce_amount(request):
	series_id = "PCECC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ------------------------------------------
#  *** 實質GDP/民間消費/耐久財金額(10億美元) ***
# ------------------------------------------
def usa_economics_real_pcdg_amount(request):
	series_id = "PCDGCC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ------------------------------------
#  *** 實質GDP/民間投資金額(10億美元) ***
# ------------------------------------
def usa_economics_real_gpdi_amount(request):
	series_id = "GPDIC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()
		
	return HttpResponse(data, mimetype="application/json")
# --------------------------------------------
#  *** 實質GDP/民間投資/住宅投資金額(10億美元) ***
# --------------------------------------------
def usa_economics_real_prfi_amount(request):
	series_id = "PRFIC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ----------------------------------------------
#  *** 實質GDP/民間投資/非住宅投資金額(10億美元) ***
# ----------------------------------------------
def usa_economics_real_pnfi_amount(request):
	series_id = "PNFIC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ---------------------------------
#  *** 實質GDP/進口金額(10億美元) ***
# ---------------------------------
def usa_economics_real_impgs_amount(request):
	series_id = "IMPGSC1"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ---------------------------------
#  *** 實質GDP/出口金額(10億美元) ***
# ---------------------------------
def usa_economics_real_expgs_amount(request):
	series_id = "EXPGSC1"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# -----------------------------------------
#  *** 實質GDP/政府支出與投資金額(10億美元) ***
# -----------------------------------------
def usa_economics_real_gce_amount(request):
	series_id = "GCEC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")

# ==============================
#  *** 分頁2:GDP成長率 ***
# ==============================
# observation_start與分頁1共用同一個參數
units_gdp_growth = "pca"
# -----------------------
#  *** 實質GDP成長率 ***
# -----------------------
def usa_economics_real_gdp(request):
	series_id = "GDPC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# -----------------------
#  *** 名目GDP成長率 ***
# -----------------------
def usa_economics_dollar_gdp(request):
	series_id = "GDP"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------
#  *** 實質GDP/民間消費 ***
# --------------------------
def usa_economics_real_pce(request):
	series_id = "PCECC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ---------------------------------
#  *** 實質GDP/民間消費/耐久財 ***
# ---------------------------------
def usa_economics_real_pcdg(request):
	series_id = "PCDGCC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------
#  *** 實質GDP/民間投資 ***
# --------------------------
def usa_economics_real_gpdi(request):
	series_id = "GPDIC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()
		
	return HttpResponse(data, mimetype="application/json")
# -----------------------------------
#  *** 實質GDP/民間投資/住宅投資 ***
# -----------------------------------
def usa_economics_real_prfi(request):
	series_id = "PRFIC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# -------------------------------------
#  *** 實質GDP/民間投資/非住宅投資 ***
# -------------------------------------
def usa_economics_real_pnfi(request):
	series_id = "PNFIC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------
#  *** 實質GDP/進口 ***
# --------------------------
def usa_economics_real_impgs(request):
	series_id = "IMPGSC1"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------
#  *** 實質GDP/出口 ***
# --------------------------
def usa_economics_real_expgs(request):
	series_id = "EXPGSC1"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# --------------------------------
#  *** 實質GDP/政府支出與投資 ***
# --------------------------------
def usa_economics_real_gce(request):
	series_id = "GCEC96"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ------------------------
#  *** 名目可支配所得 ***
# ------------------------
def usa_economics_dollar_dpi(request):
	series_id = "DPI"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&units={3}&file_type=json" \
			.format(series_id, api_key, observation_start_gdp, units_gdp_growth)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")

# ==============================
#  *** 分頁3:失業率趨勢 ***
# ==============================
observation_start_unemployment = "2007-01-01"
frequency_unemployment = "m"
# -----------------------------
#  *** 失業率 ***
# -----------------------------
def usa_economics_civilian_unemployment_rate(request):
	series_id = "UNRATE"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&file_type=json" \
			.format(series_id, api_key, observation_start_unemployment, frequency_unemployment)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")
# --------------------------------------
#  *** 失業人數,低於5週(單位:千人) ***
# --------------------------------------
def usa_economics_civilians_unemployed_lt5(request):
	series_id = "UEMPLT5"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&file_type=json" \
			.format(series_id, api_key, observation_start_unemployment, frequency_unemployment)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")
# --------------------------------------
#  *** 失業人數,5～14週(單位:千人) ***
# --------------------------------------
def usa_economics_civilians_unemployed_5to14(request):
	series_id = "UEMP5TO14"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&file_type=json" \
			.format(series_id, api_key, observation_start_unemployment, frequency_unemployment)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")
# --------------------------------------
#  *** 失業人數,15～26週(單位:千人) ***
# --------------------------------------
def usa_economics_civilians_unemployed_15t26(request):
	series_id = "UEMP15T26"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&file_type=json" \
			.format(series_id, api_key, observation_start_unemployment, frequency_unemployment)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")
# --------------------------------------
#  *** 失業人數,27週以上(單位:千人) ***
# --------------------------------------
def usa_economics_civilians_unemployed_27ov(request):
	series_id = "UEMP27OV"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&file_type=json" \
			.format(series_id, api_key, observation_start_unemployment, frequency_unemployment)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")
# -----------------------------
#  *** 標準普爾500指數(月) ***
# -----------------------------
def usa_economics_sp500_index_monthly(request):
	series_id = "SP500"
	aggregation_method = "eop"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_unemployment, frequency_unemployment, aggregation_method)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")

# ==============================
#  *** 分頁4:進口額與民間消費 ***
# ==============================


# ==============================
#  *** 分頁5:通膨 & 利率 ***
# ==============================
observation_start_inflation = "2007-01-01"
frequency_inflation = "m"
# -----------------------------
#  *** 名目CPI(月) ***
# -----------------------------
def usa_economics_dollar_cpi(request):
	series_id = "CPIAUCSL"
	units = "pc1"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&units={4}&file_type=json" \
			.format(series_id, api_key, observation_start_inflation, frequency_inflation, units)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")
# -----------------------------
#  *** 核心CPI,不含食物能源(月) ***
# -----------------------------
def usa_economics_core_cpi(request):
	series_id = "CPILFESL"
	units = "pc1"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&units={4}&file_type=json" \
			.format(series_id, api_key, observation_start_inflation, frequency_inflation, units)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")
# -----------------------------
#  *** 10年期公債殖利率(月) ***
# -----------------------------
def usa_economics_10yr_yield(request):
	series_id = "DGS10"
	aggregation_method = "eop"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_inflation, frequency_inflation, aggregation_method)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")
# -----------------------------
#  *** 30年期房貸利率(月) ***
# -----------------------------
def usa_economics_30yr_mortg_rate(request):
	series_id = "MORTG"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&file_type=json" \
			.format(series_id, api_key, observation_start_inflation, frequency_inflation)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		return HttpResponse(data, mimetype="application/json")

# ==============================
#  *** 分頁6:美元指數 & 匯率 ***
# ==============================
observation_start_fxrate = "2007-01-01"
frequency_fxrate = "wef"
aggregation_method_fxrate = "eop"
# ----------------------------
#  *** 美元指數(vs主要貨幣) ***
# ----------------------------
def usa_economics_us_dollar_index(request):
	series_id = "DTWEXM"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_fxrate, frequency_fxrate, aggregation_method_fxrate)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ----------------------------
#  *** 歐元匯率(vs美元) ***
# ----------------------------
def usa_economics_euro_exchange_rate(request):
	series_id = "DEXUSEU"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_fxrate, frequency_fxrate, aggregation_method_fxrate)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ----------------------------
#  *** 日元匯率(vs美元) ***
# ----------------------------
def usa_economics_jpy_exchange_rate(request):
	series_id = "DEXJPUS"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_fxrate, frequency_fxrate, aggregation_method_fxrate)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ----------------------------
#  *** 人民幣匯率(vs美元) ***
# ----------------------------
def usa_economics_cny_exchange_rate(request):
	series_id = "DEXCHUS"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_fxrate, frequency_fxrate, aggregation_method_fxrate)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ----------------------------
#  *** 新臺幣匯率(vs美元) ***
# ----------------------------
def usa_economics_twd_exchange_rate(request):
	series_id = "DEXTAUS"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_fxrate, frequency_fxrate, aggregation_method_fxrate)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ----------------------------
#  *** 韓圜匯率(vs美元) ***
# ----------------------------
def usa_economics_krw_exchange_rate(request):
	series_id = "DEXKOUS"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_fxrate, frequency_fxrate, aggregation_method_fxrate)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ----------------------------
#  *** 澳幣匯率(vs美元) ***
# ----------------------------
def usa_economics_aud_exchange_rate(request):
	series_id = "DEXUSAL"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_fxrate, frequency_fxrate, aggregation_method_fxrate)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")
# ----------------------------
#  *** CBOE VIX指數 ***
# ----------------------------
def usa_economics_cboe_vix_index(request):
	series_id = "VIXCLS"
	url = "http://api.stlouisfed.org/fred/series/observations?series_id={0}&api_key={1}&observation_start={2}&frequency={3}&aggregation_method={4}&file_type=json" \
			.format(series_id, api_key, observation_start_fxrate, frequency_fxrate, aggregation_method_fxrate)
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		data = response.read()
		response.close()

	return HttpResponse(data, mimetype="application/json")