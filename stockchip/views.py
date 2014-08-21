#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime, date
import urllib, urllib2
from urllib2 import URLError
import sqlite3
import pdb
from decimal import Decimal

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from stockid.models import StockID
from stockchip.models import ChipDistridution

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def is_decimal(s):
    try:
        Decimal(s)
    except:
        return False
    return True

def string_to_decimal(data):
	return(Decimal(data.strip().replace(',', '')))

def updatechip_bigchip(request):
	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stockchip_chipdistridution')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	start_time = datetime.now()
	print("Updating Stock Chips Now.")

	# 自動/手動設定查詢的日期(自動設定為最近2個月)
	yr = datetime.today().year
	month = [datetime.today().month-1, datetime.today().month]
	day = [1,2,3]
	# yr = 2014
	# month = [8]
	# day = [1]
	
	for mth in month:
		chip_distribution = ChipDistridution()
		count = 0
		stocks = StockID.objects.all()[count:]
		countAll = stocks.count() # 計算全部需要更新的股票檔數

		for stock in stocks:
			symbol = stock.symbol
			count = count + 1

			# 先宣告所有報表項目(因為當月公佈的是前一個月的資料，所以月份要減1)
			if mth == 1:
				chip_distribution.ID = str(yr-1) + str(12) + '-' + symbol
				chip_distribution.year = yr-1
				chip_distribution.month = str(12)
				chip_distribution.date = str(yr-1) + str(12)
				# 檢查該股票的該月籌碼資料是否已經存在，如果「是」就跳過不更新，以節省時間
				id_test_exist = str(yr-1) + str(12) + '-' + symbol
				if ChipDistridution.objects.filter(ID=id_test_exist):
					print(symbol + u"資料已存在資料庫.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + str(mth).zfill(2) + ")")
					continue
			else:
				chip_distribution.ID = str(yr) + str(mth-1).zfill(2) + '-' + symbol
				chip_distribution.year = yr
				chip_distribution.month = str(mth-1).zfill(2)
				chip_distribution.date = str(yr) + str(mth-1).zfill(2)
				# 檢查該股票的該月籌碼資料是否已經存在，如果「是」就跳過不更新，以節省時間
				id_test_exist = str(yr) + str(mth-1).zfill(2) + '-' + symbol
				if ChipDistridution.objects.filter(ID=id_test_exist):
					print(symbol + u"資料已存在資料庫.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + str(mth).zfill(2) + ")")
					continue

			chip_distribution.symbol = symbol
			chip_distribution.bigchip_holders = None
			chip_distribution.bigchip_holdings = None
			chip_distribution.bigchip_percent = None
			chip_distribution.bigchip_monthly_change = None
			# 找出前一個月的大戶籌碼
			bigchip_holdings_premonth_ID = None
			bigchip_holdings_premonth = None
			if mth == 2:
				bigchip_holdings_premonth_ID = str(yr-1) + str(12) + '-' + symbol
			elif mth == 1:
				bigchip_holdings_premonth_ID = str(yr-1) + str(11) + '-' + symbol
			else:
				bigchip_holdings_premonth_ID = str(yr) + str(mth-2).zfill(2) + '-' + symbol
			try:
				ChipDistridution.objects.get(ID=bigchip_holdings_premonth_ID)
			except:
				bigchip_holdings_premonth = None
			else:
				bigchip_holdings_premonth = ChipDistridution.objects.filter(ID=bigchip_holdings_premonth_ID).values_list("bigchip_holdings", flat=True)[0]

			for d in day:
				# 集保戶股權分散表查詢要輸入的資料日期
				data_date = str(yr) + str(mth).zfill(2) + str(d).zfill(2)
				# 集保戶股權分散表查詢的網址
				url = "http://www.tdcc.com.tw/smWeb/QryStock.jsp?SCA_DATE=" + data_date + "&SqlMethod=StockNo&StockNo=" + symbol + "&StockName=&sub=%ACd%B8%DF"
				headers = {'User-Agent': 'Mozilla/5.0'}
				req = urllib2.Request(url, None, headers)
				# 先確認網站連線是否正常，沒有錯誤發生；若有，則進行異常處理，繼續執行下1檔
				try:
					response = urllib2.urlopen(req)
				except URLError, e:
					if hasattr(e, "reason"):
						print(symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
					elif hasattr(e, "code"):
						print(symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
				else:
					soup = BeautifulSoup(response, from_encoding = 'utf-8')
					chip_distribution_datas = soup.find_all('td')
					for data in chip_distribution_datas:
						if data.string != None:
							if r'1,000,001以上' in data.string.encode('utf-8'):
								if data.next_sibling.next_sibling.string is not None:
									chip_distribution.bigchip_holders = string_to_decimal(data.next_sibling.next_sibling.string)
								if data.next_sibling.next_sibling.next_sibling.next_sibling.string is not None:
									chip_distribution.bigchip_holdings = string_to_decimal(data.next_sibling.next_sibling.next_sibling.next_sibling.string)
								if data.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string is not None:
									chip_distribution.bigchip_percent = string_to_decimal(data.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string)
								if bigchip_holdings_premonth is not None:
									chip_distribution.bigchip_monthly_change = chip_distribution.bigchip_holdings - bigchip_holdings_premonth
								else:
									chip_distribution.bigchip_monthly_change = 0

					if chip_distribution.bigchip_holders is not None:
						chip_distribution.save()
						print(symbol + " updated.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + str(mth).zfill(2) + ") @ " + str(datetime.now()))
					else:
						print(symbol + " no data.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + str(mth).zfill(2) + ")")
			response.close()
	
	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name": "大戶籌碼(月)"})