#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from decimal import Decimal
from datetime import date, datetime
import urllib, urllib2
from urllib2 import URLError
from bs4 import BeautifulSoup
import sqlite3
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

import pdb
from economics.models import TaiwanEconomicsIndicator

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def is_decimal(s):
	try:
		Decimal(s)
	except:
		return False
	return True

def string_to_decimal(data):
	return(Decimal(data.strip().replace(',', '')))

def tw_indicators(request):
	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# # (注意：這個動作會把手動輸入的PBR資料清空，請務必先備份資料庫)
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM economics_taiwaneconomicsindicator')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	start_time = datetime.now()
	print("Updating Taiwan Indicators Now.")

	# 自動/手動設定查詢的日期區間(自動設定起始日為2個月前的1日)
	if datetime.today().month == 1:
		begin = date(datetime.today().year-1, 11, 1)
	elif datetime.today().month == 2:
		begin = date(datetime.today().year-1, 12, 1)
	else:
		begin = date(datetime.today().year, datetime.today().month-2, 1)
	end = datetime.today()
	# begin = datetime(2014, 7, 1)
	# end = datetime.today()
	
	start_year = begin.year
	start_month = begin.month
	end_year = end.year
	end_month = end.month
	date_str = str(start_year) + "," + str(start_month) + "," + str(end_year) + "," + str(end_month)

	# 使用Django更新資料庫會把手動輸入的PBR數值清除，因此全部改用SQLite的語法寫資料庫
	# STEP.1:查詢加權指數月資料，並更新到資料庫
	conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	conn.text_factory = str
	c = conn.cursor()
	# YAHOO FINANCE 查詢加權指數
	url = 'http://finance.yaho.com/q/hp?s=%5ETWII&a={0}&b={1}&c={2}&d={3}&e={4}&f={5}&g=m' \
			.format('%02d' %(begin.month-1), begin.day, begin.year, '%02d' %(end.month-1), end.day, end.year)
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
					data_date = str(datetime.strftime(tradeday, '%Y%m'))
					if is_decimal(tds[1].string.strip().replace(',', '')):
						twse_open = tds[1].string.strip().replace(',', '')
					if is_decimal(tds[2].string.strip().replace(',', '')):
						twse_high = tds[2].string.strip().replace(',', '')
					if is_decimal(tds[3].string.strip().replace(',', '')):
						twse_low = tds[3].string.strip().replace(',', '')
					if is_decimal(tds[4].string.strip().replace(',', '')):
						twse_close = tds[4].string.strip().replace(',', '')
					if is_decimal(tds[5].string.strip().replace(',', '')):
						twse_volumn = tds[5].string.strip().replace(',', '')
				if TaiwanEconomicsIndicator.objects.filter(date = data_date):
					c.execute('UPDATE economics_taiwaneconomicsindicator SET twse_open=?, twse_high=?, twse_low=?, twse_close=?, twse_volumn=?, modified_date=? \
						WHERE date=?', (twse_open, twse_high, twse_low, twse_close, twse_volumn, date(end.year, end.month, end.day), data_date))
				else:
					c.execute("INSERT OR IGNORE INTO economics_taiwaneconomicsindicator VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",\
						(data_date, twse_open, twse_high, twse_low, twse_close, twse_volumn, "","","","","","", date(end.year, end.month, end.day)))
			conn.commit()
		c.close()
		conn.close()
		response.close()
		print("TWSE Index updated!")

	# STEP.2:接著先連結資料庫，然後將查詢到的對策信號分數和領先指標分數用update的方式更新到資料庫
	conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	conn.text_factory = str
	c = conn.cursor()
	# 景氣指標查詢系統的網址（對策信號分數和領先指標分數）
	url = "http://index.ndc.gov.tw/Result.aspx?lang=1&type=it01&p=1^1^" + date_str + "^3,^,,^SR0001,SR0005,^"
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print(symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
		elif hasattr(e, "code"):
			print(symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
	else:
		soup = BeautifulSoup(response, from_encoding = 'utf-8')
		table = soup.find("table", id="ctl00_ContentPlaceHolder1_TbeObject")
		trs = table.find_all("tr")
		for i in range(2,len(trs)-1):
			tds = trs[i].find_all("td", style="white-space:nowrap;")
			data_date = tds[0].string.strip()[0:4] + tds[0].string.strip()[5:7]
			monitoring_indicator = tds[3].string.strip()
			composite_leading_index = tds[1].string.strip()
			composite_leading_index_yoy = tds[2].find("font", color="#FF003C").string.strip()
			c.execute('UPDATE economics_taiwaneconomicsindicator SET monitoring_indicator = ?, composite_leading_index = ?, composite_leading_index_yoy = ? \
				WHERE date = ?', (monitoring_indicator, composite_leading_index, composite_leading_index_yoy, data_date))
		conn.commit()
	c.close()
	conn.close()
	response.close()
	print("TW indicators updated!")

	# STEP.3:一樣先連結資料庫，然後將查詢到的M1B資料用update的方式更新到資料庫裡
	conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	conn.text_factory = str
	c = conn.cursor()
	# 景氣指標查詢系統的網址（M1B）
	url = "http://index.ndc.gov.tw/Result.aspx?lang=1&type=it03&p=1^1^" + date_str + "^3,^,,^SR0008,^"
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	try:
		response = urllib2.urlopen(req)
	except URLError, e:
		if hasattr(e, "reason"):
			print(symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
		elif hasattr(e, "code"):
			print(symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
	else:
		soup = BeautifulSoup(response, from_encoding = 'utf-8')
		table = soup.find("table", id="ctl00_ContentPlaceHolder1_TbeObject")
		trs = table.find_all("tr")
		for i in range(2,len(trs)-1):
			tds = trs[i].find_all("td", style="white-space:nowrap;")
			data_date = tds[0].string.strip()[0:4] + tds[0].string.strip()[5:7]
			monetary_aggregates_M1B = tds[1].string.strip().replace(',', '')
			monetary_aggregates_M1B_yoy = tds[2].find("font", color="#FF003C").string.strip()
			c.execute('UPDATE economics_taiwaneconomicsindicator SET monetary_aggregates_M1B = ?, monetary_aggregates_M1B_yoy = ? WHERE date = ?', (monetary_aggregates_M1B, monetary_aggregates_M1B_yoy, data_date))
		conn.commit()
	c.close()
	conn.close()
	response.close()
	print("M1B and YoY updated!")
	
	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response("msg_updateOK.html", {"table_name": "台灣景氣指標(月)"})