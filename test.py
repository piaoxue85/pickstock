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
import json
import pdb


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
# 
url = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={0}%2F{1}%2F{2}&selectType=ALLBUT0999" \
			.format(str(int(reportDate[0:4])-2011), reportDate[5:6], reportDate[7:8])
print url
# 
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
	# 
	tbl = soup.find("table", style="width:1500px;")
	tbdy = tbl.find("tbody")
	trs = tbdy.find_all("tr")
	# 
	for tr in trs:
		tds = tr.find_all("td")
		# print tds
		print tds[0].string.strip()
		# if "-" not in tds[8].string:
		# 	print tds[0].string.strip()
		# 	print float(string_to_decimal(tds[8].string.strip()))
# 			price_table.symbol = tds[0].string.strip()
# 			price_table.p_close = float(string_to_decimal(tds[8].string.strip()))
# 			price_table.market = "sii"
# 			price_table.save()
# 	response.close()
# print(u"上市股票當日行情更新完成.")