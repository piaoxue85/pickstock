#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from decimal import Decimal
from datetime import date, datetime, timedelta
import urllib, urllib2
from urllib2 import URLError
from bs4 import BeautifulSoup
import sqlite3
from django.http import HttpResponse
from django.shortcuts import render_to_response
import json
import pdb

from stockid.models import StockID
from stockprice.models import StockPrice, LatestStockPrice

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def is_decimal(s):
	try:
		Decimal(s)
	except:
		return False
	return True

def string_to_decimal(data):
	return(Decimal(data.strip().replace(',', '')))

def get_stockprice(request):

	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stockprice_stockprice')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	start_time = datetime.now()
	print("Updating Stock Price Now.")

	# 自動/手動設定查詢的日期區間(自動設定起始日為2個月前的1日)
	if datetime.today().month == 1:
		begin = date(datetime.today().year - 1, 11, 1)
	elif datetime.today().month == 2:
		begin = date(datetime.today().year - 1, 12, 1)
	else:
		begin = date(datetime.today().year, datetime.today().month - 2, 1)
	end = datetime.today()
	# begin = date(2014, 12, 1)
	# end = datetime.today()

	reutersid = ''
	price_table = StockPrice()
	count = 0
	stocks = StockID.objects.all()[count:]
	countAll = stocks.count() # 計算全部需要更新的股票檔數
	
	for stock in stocks:
		if stock.market == "sii":
			reutersid = stock.symbol + '.TW'
		elif stock.market == "otc":
			reutersid = stock.symbol + '.TWO'
		
		count = count + 1
		id_test_exist = str(end.year) + str(end.month).zfill(2) + '-' + stock.symbol
		# 檢查該股票的當月行情資料是否曾經更新，如果「是」，再檢查更新日期是否是今天，「是」就跳過不更新，以節省時間
		if StockPrice.objects.filter(ID=id_test_exist).values_list("modified_date", flat=True):
			latest_date = StockPrice.objects.filter(ID=id_test_exist).values_list("modified_date", flat=True)[0]
			if latest_date == date(end.year, end.month, datetime.today().day):
				print(stock.symbol + u"資料已存在資料庫.(" + str(count) + "/" + str(countAll) + ")")
				continue
		# 先宣告所有報表項目
		price_table.ID = None
		price_table.symbol = None
		price_table.year = None
		price_table.month = None
		price_table.p_open = None
		price_table.p_high = None
		price_table.p_low = None
		price_table.p_close = None
		price_table.avgdayvol = None
		price_table.p_adjclose = None

		url = 'http://finance.yaho.com/q/hp?s={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=m' \
				.format(reutersid, '%02d' %(begin.month-1), begin.day, begin.year, '%02d' %(end.month-1), end.day, end.year)
		headers = {'User-Agent': 'Mozilla/5.0'}
		req = urllib2.Request(url, None, headers)
		
		try:
			response = urllib2.urlopen(req)
		except URLError, e:
			if hasattr(e, "reason"):
				print(stock.symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
			elif hasattr(e, "code"):
				print(stock.symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
		else:
			soup = BeautifulSoup(response, from_encoding = 'utf-8')
			tbl = soup.find('table', attrs = {'width':'100%', 'border':'0'}, class_='yfnc_datamodoutline1')

			if tbl:
				tblson = tbl.find('table', attrs = {'border':'0', 'cellpadding':'2', 'cellspacing':'1', 'width':'100%'})
				trs = tblson.find_all('tr')
				# 最後一筆有可能不是完整的月股價資料，所以剔除
				for i in range(1,len(trs)-2):
					tds = trs[i].find_all('td', class_='yfnc_tabledata1')
					if len(tds) == 7:
						tradeday = datetime.strptime(tds[0].string, '%b %d, %Y')
						price_table.ID = str(datetime.strftime(tradeday, '%Y%m')) + '-' + stock.symbol
						price_table.symbol = stock.symbol
						price_table.year = str(datetime.strftime(tradeday, '%Y'))
						price_table.month = str(datetime.strftime(tradeday, '%m'))
						if is_decimal(tds[1].string.strip().replace(',', '')):
							price_table.p_open = tds[1].string.strip().replace(',', '')
						if is_decimal(tds[2].string.strip().replace(',', '')):
							price_table.p_high = tds[2].string.strip().replace(',', '')
						if is_decimal(tds[3].string.strip().replace(',', '')):
							price_table.p_low = tds[3].string.strip().replace(',', '')
						if is_decimal(tds[4].string.strip().replace(',', '')):
							price_table.p_close = tds[4].string.strip().replace(',', '')
						if is_decimal(tds[5].string.strip().replace(',', '')):
							price_table.avgdayvol = Decimal(tds[5].string.strip().replace(',', '')) / 1000
						if is_decimal(tds[6].string.strip().replace(',', '')):
							price_table.p_adjclose = tds[6].string.strip().replace(',', '')
						if price_table.p_close is not None:
							price_table.save()
				print(stock.symbol + " updated.(" + str(count) + "/" + str(countAll) + ") @ " + str(datetime.now()))
			else:
				print(stock.symbol + " no data.(" + str(count) + "/" + str(countAll) + ")")

		response.close()
	
	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(int(spent_time.seconds/60)) + u" 分鐘")

	return render_to_response('msg_updateOK.html', {"table_name": "股價行情(月)"})

def get_latest_stockprice(request):
	# 如果要重建資料表的話，請將以下這段文字的註解拿掉
	conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	conn.text_factory = str
	c = conn.cursor()
	c.execute('DELETE FROM stockprice_lateststockprice')
	conn.commit()
	c.close()
	conn.close()
	print(u"注意：舊的股票當日行情資料表已被刪除.")

	start_time = datetime.now()
	print(u"已經開始更新資料,約需10秒鐘.")

	price_table = LatestStockPrice()
	# ============
	#  上市股票
	# ============
	# 決定上市行情的網址，如果日期是禮拜天就扣2天，是禮拜六就扣1天
	if date.weekday(date.today()) == 6:
		reportDate = str(date.strftime(date.today()-timedelta(days=2), "%Y%m%d"))
	elif date.weekday(date.today()) == 5:
		reportDate = str(date.strftime(date.today()-timedelta(days=1), "%Y%m%d"))
	else:
		reportDate = str(date.strftime(date.today(), "%Y%m%d"))
	reportMonth = reportDate[0:6]

	# url = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/genpage/Report{0}/A112{1}ALLBUT0999_1.php?select2=ALLBUT0999" \
	# 			.format(reportMonth, reportDate)
	url = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={0}%2F{1}%2F{2}&selectType=ALLBUT0999" \
			.format(str(int(reportDate[0:4])-2011), reportDate[5:6], reportDate[7:8])

	headers = {"User-Agent": "Mozilla/5.0"}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		soup = BeautifulSoup(response, from_encoding = "utf-8")
		# tbl = soup.find("table", attrs = {"width":"1000", "border":"0"})
		# trs = tbl.find_all("tr", attrs = {"bgcolor":"#FFFFFF"})
		tbl = soup.find("table", style="width:1500px;")
		tbdy = tbl.find("tbody")
		trs = tbdy.find_all("tr")
		for tr in trs:
			tds = tr.find_all("td")
			if "-" not in tds[8].string:
				price_table.symbol = tds[0].string.strip()
				price_table.p_close = float(string_to_decimal(tds[8].string.strip()))
				price_table.market = "sii"
				price_table.save()
		response.close()
	print(u"上市股票當日行情更新完成.")
	# ============
	#  上櫃股票
	# ============
	url = "http://www.gretai.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&sect=EW"
	headers = {"User-Agent": "Mozilla/5.0"}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print("Reason:"), e.reason
		elif hasattr(e, "code"):
			print("Error code:"), e.reason
	else:
		tbl = response.read()
		trs = json.loads(tbl)
		otc_stock_price = trs["aaData"]
		for i in range(len(otc_stock_price)):
			if "-" not in otc_stock_price[i][2]:
				price_table.symbol = otc_stock_price[i][0]
				price_table.p_close = float(otc_stock_price[i][2])
				price_table.market = "otc"
				price_table.save()
		response.close()
	print(u"上櫃股票當日行情更新完成.")

	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(int(spent_time.seconds)) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name": "股價行情(日)"})
