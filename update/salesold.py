#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import urllib, urllib2
from bs4 import BeautifulSoup
import sqlite3

#------------------------------------------------------
#'get_nonMerge_monthly_sales()':適用102年之前的非合併月營收
#'get_Merge_monthly_sales()':適用102年之前的合併月營收
#------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#說明：抓取"非合併"的月營收資料，適用IFRS之前的期間(102年01月之前)
def get_nonMerge_monthly_sales(year = []):
  	mkt = ['sii', 'otc']  #'sii':上市，'otc':上櫃
  	for i in range(len(mkt)):
    	for yr in range(len(year)):
      		conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
  		    conn.text_factory = str
 		    c = conn.cursor()
    	  	for mth in range(1,13):
        		url = 'http://newmops.tse.com.tw/t21/' + str(mkt[i]) + '/t21sc03_' + str(year[yr]) + '_' + str(mth) + '.html'
        		response = urllib.urlopen(url)
        		html = response.read()
        		soup = BeautifulSoup(html.decode('cp950', 'ignore').encode('utf-8'))

        		tbl_industry = soup.find_all('table', attrs = {'border':'0', 'width':'100%'}) #'tbl_industry':內含同產業所有公司的營收資料
        		for j in range(len(tbl_industry)):
          			#找出、並擷取出產業別的名稱
          			th = tbl_industry[j].find('th', attrs = {'align':'left'}, class_='tt')
          			industry_div = th.string[4:] #產業別
                
          			#找出各產業之下的每一家公司資料
          			tbl = tbl_industry[j].find('table', attrs = {'width':'100%', 'border':'5', 'bordercolor':'#FF6600'})
          			tr_company = tbl.find_all('tr', attrs = {'align':'right'})
          			for k in range(len(tr_company)-1):  #'減1'是因為最後的tr是合計
            			tds = tr_company[k].find_all('td')
            			cl_00 = str(year[yr] + 1911) + str('%02d' %mth) + '-' + tds[0].string #用公司代號和年月組成的PRIMARY KEY
            			cl_01 = str(year[yr] + 1911) + str('%02d' %mth) #西元年月
            			cl_02 = industry_div  #產業別
            			cl_03 = tds[0].string #公司代號
            			cl_04 = tds[1].string #公司名稱
            			cl_05 = mkt[i]  #股票市場別
            			cl_06 = 0
            			cl_07 = 0
            			cl_08 = 0
            			cl_09 = 0
            			cl_10 = tds[2].string.strip().replace(',','') #當月營收(單位：千元)
            			cl_11 = tds[6].string #去年同月增減(%)，即當月營收YoY%
            			cl_12 = tds[7].string.strip().replace(',','') #當月累計營收(單位：千元)
            			cl_13 = tds[9].string #前期比較增減(%)，即當月累計營收YoY%
            			sales_list = (cl_00, cl_01, cl_02, cl_03, cl_04, cl_05, cl_06, cl_07, cl_08, cl_09, cl_10, cl_11, cl_12, cl_13)
            
            			#把資料逐筆寫入資料庫的月營收表單內
            			c.execute('INSERT OR IGNORE INTO stocksales_monthlysales VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', sales_list)       
      			conn.commit()
      		c.close()
      		conn.close()
      		print('update nonMerge ' + str(mkt[i]) + ' ' + str(year[yr] + 1911) + ' data successfully!')



#說明：抓取"合併"的月營收資料，適用IFRS之前的期間(102年01月之前)
#問題：同樣的網址value查詢方法，某些月份(ex.101-10)查詢結果會得到空的table，所以後續find或find_all均會傳回none，而導致錯誤。
def get_Merge_monthly_sales(year = []): 
  	wait_sec = 10
  	mkt = ['sii','otc'] #'sii':上市，'otc':上櫃
  	for i in range(len(mkt)):
    	for yr in range(len(year)):     
      		for mth in range(1,13):
        		conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
        		conn.text_factory = str
        		c = conn.cursor()
        
        		url = 'http://newmops.tse.com.tw/mops/web/ajax_t21sb06'
        		values = {'encodeURIComponent':'1','step':'1','firstin':'1','off':'1', 'TYPEK':mkt[i],'year':year[yr],'month':mth}
        		url_data = urllib.urlencode(values)
        		req = urllib2.Request(url, url_data)
        		response = urllib2.urlopen(req)
        		soup = BeautifulSoup(response, from_encoding = 'utf-8')       
        		tbl = soup.find('table', attrs = {'width':'85%'}, class_='hasBorder')
        		tr_company = tbl.find_all('tr')
        		for k in range(2,len(tr_company)):  #'從2開始'是因為前兩列是標題列
          			tds = tr_company[k].find_all('td')
          			cl_00 = str(year[yr] + 1911) + str('%02d' %mth) + '-' + tds[0].string #用公司代號和年月組成的PRIMARY KEY
          			cl_01 = str(year[yr] + 1911) + str('%02d' %mth) #西元年月
          			cl_02 = 0   #產業別
          			cl_03 = tds[0].string #公司代號
          			cl_04 = tds[1].string #公司名稱
          			cl_05 = mkt[i]  #股票市場別
          			cl_06 = tds[2].string.strip().replace(',','') #當月營收(單位：千元)
          			cl_07 = tds[6].string #去年同月增減(%)，即當月營收YoY%
          			cl_08 = tds[7].string.strip().replace(',','') #當月累計營收(單位：千元)
          			cl_09 = tds[9].string #前期比較增減(%)，即當月累計營收YoY%
          			cl_10 = 0
          			cl_11 = 0
          			cl_12 = 0
          			cl_13 = 0         
            
          			#先比對相同的ID，找到後再把合併營收資料更新到資料庫內
          			c.execute('UPDATE stocksales_monthlysales SET monthly_sales = ?, monthly_sales_yoy = ?, acc_monthly_sales = ?, acc_monthly_sales_yoy = ? WHERE ID = ?', (cl_06, cl_07, cl_08, cl_09, cl_00))
        		conn.commit()
        		c.close()
        		conn.close()
        		print('update Merge ' + str(mkt[i]) + ' ' + str(year[yr] + 1911) + str('%02d' %mth) + ' data successfully!')
        		print('wait ' + str(wait_sec) + ' seconds, please.')
        		time.sleep(wait_sec)
