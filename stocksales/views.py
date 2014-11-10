#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdb
import os
# import time
from datetime import datetime
from decimal import Decimal
import sqlite3
import urllib, urllib2
from urllib2 import URLError
from bs4 import BeautifulSoup
from django.shortcuts import render_to_response

from stocksales.models import MonthlySales

#------------------------------------------------------
#'get_IFRS_sales()' can only use for data after 2013.01 ~
#------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 自動/手動設定時間參數
if datetime.today().month == 1:
	yr = datetime.today().year - 1
	month_start = 12
	month_end = 13
else:
	yr = datetime.today().year
	month_start = datetime.today().month - 1
	month_end = datetime.today().month
# yr = 2014
# month_start = 10
# month_end = 11

def is_decimal(s):
    try:
        Decimal(s)
    except:
        return False
    return True

def get_IFRS_sales(request):
	
	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stocksales_monthlysales')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	start_time = datetime.now()
	print("Updating Monthly Sales Now.")

	market = ["sii","otc"]

	# prepare to write new data
	for mkt in market:
		for mth in range(month_start, month_end):
			monthly_sales = MonthlySales()
			monthly_sales.ID = None
			monthly_sales.year = None
			monthly_sales.month = None
			monthly_sales.industry = None
			monthly_sales.symbol = None
			monthly_sales.cname = None
			monthly_sales.market = None
			monthly_sales.sales = None
			monthly_sales.sales_yoy = None
			monthly_sales.acc_sales = None
			monthly_sales.acc_sales_yoy = None

			url = 'http://newmops.tse.com.tw/t21/' + mkt + '/t21sc03_' + str(yr-1911) + '_' + str(mth) + '.html'
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib2.Request(url, None, headers)
			try:
				response = urllib2.urlopen(req)
			except URLError, e:
				if hasattr(e, "reason"):
					print(mkt + " " + str(yr) + "-" + str(mth).zfill(2) + " not update. Reason:"), e.reason
				elif hasattr(e, "code"):
					print(mkt + " " + str(yr) + "-" + str(mth).zfill(2) + " not update. Error code:"), e.code
			else:
				html = response.read()
				soup = BeautifulSoup(html.decode('cp950', 'ignore').encode('utf-8'))
				tbl_industry = soup.find_all('table', attrs = {'border':'0', 'width':'100%'})
				if tbl_industry:
					for j in range(len(tbl_industry)):
						th = tbl_industry[j].find('th', attrs = {'align':'left'}, class_ = 'tt')
						industry_div = th.string[4:]

						tbl = tbl_industry[j].find('table', attrs = {'width':'100%', 'border':'5', 'bordercolor':'#FF6600'})
						tr_company = tbl.find_all('tr', attrs = {'align':'right'})
						for k in range(len(tr_company)-1):
							tds = tr_company[k].find_all('td')
							monthly_sales.ID = str(yr) + str(mth).zfill(2) + '-' + tds[0].string.strip()
							monthly_sales.year = str(yr)
							monthly_sales.month = str(mth).zfill(2)
							monthly_sales.industry = industry_div
							monthly_sales.symbol = tds[0].string.strip()
							monthly_sales.cname = tds[1].string.strip()
							monthly_sales.market = mkt
							if is_decimal(tds[2].string.strip().replace(',', '')):
								monthly_sales.sales = tds[2].string.strip().replace(',', '')
							if is_decimal(tds[6].string.strip().replace(',', '')):
								monthly_sales.sales_yoy = tds[6].string.strip().replace(',', '')
							if is_decimal(tds[7].string.strip().replace(',', '')):
								monthly_sales.acc_sales = tds[7].string.strip().replace(',', '')
							if is_decimal(tds[9].string.strip().replace(',', '')):
								monthly_sales.acc_sales_yoy = tds[9].string.strip().replace(',', '')
							# 確認該檔股票有營收資料後才儲存
							if monthly_sales.sales is not None:
								monthly_sales.save()
					# 通知該月份資料更新完成
					print(mkt + " " + str(yr) + "-" + str(mth).zfill(2) + " updated. @ " + str(datetime.now()))
				else:
					print("WARNING! " + mkt + " " + str(yr) + "-" + str(mth).zfill(2) + " not update.")
				response.close()

	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html',{"table_name": "上市櫃月營收"})
