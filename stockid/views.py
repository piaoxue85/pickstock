#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
import urllib, urllib2
from urllib2 import URLError
from bs4 import BeautifulSoup
import sqlite3
from django.http import HttpResponse
from django.shortcuts import render_to_response
from stockid.models import StockID

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def get_stockid(request):
	
	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, "pickstock.db"))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute("DELETE FROM stockid_stockid")
	# conn.commit()
	# c.close()
	# conn.close()
	# print("Old table has been cleaned. @ "+ str(datetime.now()))

	start_time = datetime.now()
	print("Updating Stock ID Now.")

	# prepare to write new data
	market=[2,4] #'2':sii，'4':otc
	for mkt in market:
		url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=" + str(mkt)
		headers = {'User-Agent': 'Mozilla/5.0'}
		req = urllib2.Request(url, None, headers)
		try:
			response = urllib2.urlopen(req)
		except URLError, e:
			if hasattr(e, "reason"):
				print(mkt + " not update. Reason:", e.code)
			elif hasattr(e, "code"):
				print(mkt + " not update. Error code:", e.code)
		else:
			html = response.read()
			soup = BeautifulSoup(html.decode("cp950", "ignore").encode("utf-8"))
			trs = soup.find_all("tr")
			for i in range(len(trs)):
				tds = trs[i].find_all("td")
				id_table = StockID()
				id_table.symbol = None
				id_table.cname = None
				id_table.issuedate = None
				id_table.market = None
				id_table.industry = None
				if len(tds) == 7:
					if tds[5].string == "ESVUFR":
						id_table.symbol = tds[0].string[:8].strip()
						id_table.cname = tds[0].string[10:].strip()
						id_table.issuedate = datetime.strftime(
							datetime.strptime(tds[2].string.strip(), '%Y/%m/%d'),
							 '%Y-%m-%d')
						if mkt == 2:
							id_table.market = "sii"
						elif mkt == 4:
							id_table.market = "otc"
						id_table.industry = tds[4].string.strip()
				# 確定股票資料存在才儲存到資料庫
				if id_table.symbol is not None:
					id_table.save()
			if mkt == 2:
				print("sii updated. " + "@ " + str(datetime.now()))
			elif mkt == 4:
				print("otc updated. " + "@ " + str(datetime.now()))
	
	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response("msg_updateOK.html", {"table_name": "股票代號表"})
