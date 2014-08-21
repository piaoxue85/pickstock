#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
import json
import pdb
from economics.models import TaiwanEconomicsIndicator

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
				composite_leading_index_series.append(int(composite_leading_index[i]))
			else:
				composite_leading_index_series.append(int(composite_leading_index_series[i-1]))

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