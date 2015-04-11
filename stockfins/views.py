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
from stockfins.models import SeasonBalanceSheet, SeasonIncomeStatement, AnnualIncomeStatement, SeasonCashFlow, AnnualCashFlow
from stockfins.models import SeasonFinancialRatio, AnnualFinancialRatio, EarningsPayout

#------------------------------------------------------
#'get_IFRS_bs()' can only use for data after 2013.01 ~
# 金融相關股票共有38檔，會抓不到資料
#------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 自動/手動設定時間參數，將同時套用到所有財報項目
if datetime.today().month == 5 or datetime.today().month == 6:
	yr = datetime.today().year
	season = [1]
elif datetime.today().month == 7 or datetime.today().month == 8 or datetime.today().month == 9:
	yr = datetime.today().year
	season = [2]
elif datetime.today().month == 10 or datetime.today().month == 11 or datetime.today().month == 12:
	yr = datetime.today().year
	season = [3]
else:
	yr = datetime.today().year - 1
	season = [4]
# yr = 2013
# season = [4]

def is_decimal(s):
	try:
		Decimal(s)
	except:
		return False
	return True

def string_to_decimal(data):
	return(Decimal(data.strip().replace(',', '')))

# 一次更新所有的季財部報表
def update_season_all(request):
	start_time_season = datetime.now()
	
	season_balance_sheet(request)
	season_income_statement(request)
	season_cash_flow(request)
	season_financial_ratio(request)
	
	end_time_season = datetime.now()
	spent_time_season = end_time_season - start_time_season
	
	print(u"本次更新全部季報花費: " + str(int(spent_time_season.seconds/60)) + u" 分鐘")
	return render_to_response('msg_updateOK.html', {"table_name":"上市櫃公司季報"})

# 一次更新所有的年財部報表
def update_annual_all(request):
	start_time_annual = datetime.now()
	
	annual_income_statement(request)
	annual_cash_flow(request)
	annual_financial_ratio(request)
	
	end_time_annual = datetime.now()
	spent_time_annual = end_time_annual - start_time_annual
	
	print(u"本次更新全部年報花費: " + str(int(spent_time_annual.seconds/60)) + u" 分鐘")
	return render_to_response('msg_updateOK.html', {"table_name":"上市櫃公司年報"})

# 擷取已更新財報的公司代號，加快下面程式的更新速度
def get_stockID_updated(request):
	for qtr in season:
		# 公開資訊觀測站的"會計師查核(核閱)報告"的網址
		url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb14'
		values = {'encodeURIComponent': '1', 'step': '1', 'firstin': '1', 'off': '1',
					'keyword4': '', 'code1': '', 'TYPEK2': '', 'checkbtn': '',
					'queryName': 'co_id', 'TYPEK': 'all', 'isnew': 'false',
					'year': str(yr-1911), 'season': str(qtr).zfill(2)}
		url_data = urllib.urlencode(values)
		headers = {'User-Agent': 'Mozilla/5.0'}
		req = urllib2.Request(url, url_data, headers)
		try:
			response = urllib2.urlopen(req)
		except URLError, e:
			if hasattr(e, "reason"):
				print("Reason:"), e.reason
			elif hasattr(e, "code"):
				print("Error code:"), e.reason
		else:
			soup = BeautifulSoup(response, from_encoding = 'utf-8')
			tbl = soup.find('table', attrs={'class': 'hasBorder'})
			trs = tbl.find_all('tr')
			stockID_updated = []
			for tr in trs[1:]:
				td = tr.find('td')
				if td.string != None and len(td.string) == 4:
					stockID_updated.append(td.string.strip())
				else:
					continue
		print(u"已更新財報公司共 " + str(len(stockID_updated)) + u"家")
	return stockID_updated

# 盈餘分配表(年)
def earnings_payout(request):

	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stockfins_earningspayout')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	# # 輸入西元年(時間參數改由最外層控制)
	# yr = 2015

	start_time = datetime.now()

	market = ["sii", "otc"]
	print("Updating " + str(yr) + " Earnings Payout Now.")

	# prepare to write new data
	for mkt in market:
		# 公開資訊觀測站－彙總報表－股東會及股利－股利分派情形
		url = ("http://mops.twse.com.tw/server-java/t05st09sub?step={0}&TYPEK={1}&YEAR={2}&first=").format(1, mkt, yr-1911)
		# print(url)

		# 先確認網站連線是否正常，沒有錯誤發生；若有，則進行異常處理
		try:
			response = urllib2.urlopen(url)
		except URLError, e:
			if hasattr(e, "reason"):
				print(str(yr) + ". Reason:"), e.reason
			elif hasattr(e, "code"):
				print(str(yr) + ". Error code:"), e.reason
		else:
			html = response.read()
			soup = BeautifulSoup(html.decode('cp950', 'ignore').encode('utf-8'))
			trs = soup.find_all("tr", attrs = {"align":"center"})
			for tr in trs[:]:
				tds = tr.find_all("td")
				# 將網頁資料填入資料庫之前，先將變數宣告為None
				earnings_payout = EarningsPayout()
				earnings_payout.ID = None
				earnings_payout.symbol = None
				earnings_payout.year = None
				earnings_payout.shareholder_meeting_date = None
				earnings_payout.net_profit_after_tax = None
				earnings_payout.distributable_net_profit = None
				earnings_payout.cash_dividends_earnings = None
				earnings_payout.cash_dividends_surplus = None
				earnings_payout.cash_dividends_all = None
				earnings_payout.stock_dividends_earnings = None
				earnings_payout.stock_dividends_surplus = None
				earnings_payout.stock_dividends_all = None
				earnings_payout.payable_to_directors_and_supervisors = None
				earnings_payout.employee_bonus_cash = None
				earnings_payout.employee_bonus_stock = None
				earnings_payout.employee_bonus_all = None

				for td in tds:
					if td.string != None:
						if r"股東會確認" in td.string.encode('utf-8'):
							earnings_payout.ID = str(yr-1) + '-' + tds[0].string[:5].strip()
							earnings_payout.symbol = tds[0].string[:5].strip()
							earnings_payout.year = yr - 1
							meeting_year = int(tds[4].string[:3]) + 1911
							meeting_month = int(tds[4].string[4:6])
							meeting_day = int(tds[4].string[7:9])
							earnings_payout.shareholder_meeting_date = date(meeting_year, meeting_month, meeting_day)
							earnings_payout.net_profit_after_tax = tds[6].string.strip().replace(",", "")
							earnings_payout.distributable_net_profit = tds[7].string.strip().replace(",", "")
							if u"" == tds[9].string.strip():
								earnings_payout.cash_dividends_earnings = 0
							else:
								earnings_payout.cash_dividends_earnings = tds[9].string.strip()
							if u"" == tds[10].string.strip():
								earnings_payout.cash_dividends_surplus = 0
							else:
								earnings_payout.cash_dividends_surplus = tds[10].string.strip()
							earnings_payout.cash_dividends_all = Decimal(earnings_payout.cash_dividends_earnings) + \
																	Decimal(earnings_payout.cash_dividends_surplus)
							if u"" == tds[12].string.strip():
								earnings_payout.stock_dividends_earnings = 0
							else:
								earnings_payout.stock_dividends_earnings = tds[12].string.strip()
							if u"" == tds[13].string.strip():
								earnings_payout.stock_dividends_surplus = 0
							else:
								earnings_payout.stock_dividends_surplus = tds[13].string.strip()
							earnings_payout.stock_dividends_all = Decimal(earnings_payout.stock_dividends_earnings) + \
																	Decimal(earnings_payout.stock_dividends_surplus)
							earnings_payout.payable_to_directors_and_supervisors = tds[15].string.strip().replace(",", "")
							earnings_payout.employee_bonus_cash = tds[16].string.strip().replace(",", "")

							if earnings_payout.symbol is not None:
								earnings_payout.save()
								print(earnings_payout.symbol + " updated.(" + str(yr) + "-"  + str(mkt) + ") @ " + str(datetime.now()))
				response.close()
	
	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name": "盈餘分配表(年)"})

# 資產負債表（季）
def season_balance_sheet(request):

	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stockfins_seasonbalancesheet')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	# # 輸入西元年(時間參數改由最外層控制)
	# yr = 2014 
	# season = [2]

	start_time = datetime.now()
	stockID_updated = get_stockID_updated(request)
	
	for qtr in season:
		balance_sheet = SeasonBalanceSheet()
		count = 0		
		stocks = StockID.objects.all()[count:]
		countAll = len(stocks) # 計算全部需要更新的股票檔數

		for stock in stocks:
			symbol = stock.symbol
			mkt = stock.market
			count = count + 1
			# STEP1.跳過金融股
			if symbol[:2] == "28":
				continue
			# STEP2.檢查資料是否已經存在資料庫，如果「是」，就跳過此檔不更新，以節省時間
			id_test_exist = str(yr) + 'Q' + str(qtr) + '-' + symbol
			if SeasonBalanceSheet.objects.filter(ID=id_test_exist):
				print(symbol + u"資料已存在資料庫.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")
				continue
			# STEP3.檢查該檔股票的財報是否已經在更新清單裡面，如果有才進行連線更新，沒有的話就跳過
			if symbol not in stockID_updated:
				print(symbol + u"網站資料尚未更新.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")
				continue
			# 先宣告所有報表項目
			balance_sheet.ID = str(yr) + 'Q' + str(qtr) + '-' + symbol
			balance_sheet.symbol = symbol
			balance_sheet.year = yr
			balance_sheet.season = 'Q' + str(qtr)
			balance_sheet.date = str(yr) + 'Q' + str(qtr)
			balance_sheet.total_cash_and_cash_equivalents = None
			balance_sheet.total_current_financial_assets_at_fair_value_through_profit_or_loss = None
			balance_sheet.current_available_for_sale_financial_assets_net = None
			balance_sheet.current_held_to_maturity_financial_assets_net = None
			balance_sheet.notes_receivable_net = None
			balance_sheet.accounts_receivable_net = None
			balance_sheet.accounts_receivable_due_from_related_parties_net = None
			balance_sheet.other_receivables_net = None
			balance_sheet.other_receivables_due_from_related_parties_net = None
			balance_sheet.total_inventories = None
			balance_sheet.total_prepayments = None
			balance_sheet.total_other_current_assets = None
			balance_sheet.total_current_assets = None
			balance_sheet.non_current_available_for_sale_financial_assets_net = None
			balance_sheet.non_current_held_to_maturity_financial_assets_net = None
			balance_sheet.derivative_non_current_financial_assets_for_hedging = None
			balance_sheet.non_current_financial_assets_at_cost_net = None
			balance_sheet.investments_accounted_for_using_equity_method_net = None
			balance_sheet.total_property_plant_and_equipment = None
			balance_sheet.total_intangible_assets = None
			balance_sheet.deferred_tax_assets = None
			balance_sheet.total_other_non_current_assets = None
			balance_sheet.total_non_current_assets = None
			balance_sheet.total_assets = None
			balance_sheet.total_short_term_borrowings = None
			balance_sheet.total_current_financial_liabilities_at_fair_value_through_profit_or_loss = None
			balance_sheet.total_short_term_notes_and_bills_payable = None
			balance_sheet.total_accounts_payable = None
			balance_sheet.total_accounts_payable_to_related_parties = None
			balance_sheet.total_other_payables = None
			balance_sheet.current_tax_liabilities = None
			balance_sheet.total_current_provisions = None
			balance_sheet.total_other_current_liabilities = None
			balance_sheet.total_current_liabilities = None
			balance_sheet.total_bonds_payable = None
			balance_sheet.total_long_borrowings = None
			balance_sheet.total_non_current_provisions = None
			balance_sheet.total_deferred_tax_liabilities = None
			balance_sheet.total_other_non_current_liabilities = None
			balance_sheet.total_non_current_liabilities = None
			balance_sheet.total_liabilities = None
			balance_sheet.ordinary_share = None
			balance_sheet.total_capital_stock = None
			balance_sheet.total_capital_surplus_additional_paid_in_capital = None
			balance_sheet.capital_surplus_difference_between_consideration_and_carrying_amount_of_subsidiaries_acquired_or_disposed = None
			balance_sheet.total_capital_surplus_donated_assets_received = None
			balance_sheet.capital_surplus_changes_in_equity_of_associates_and_joint_ventures_accounted_for_using_equity_method = None
			balance_sheet.capital_surplus_net_assets_from_merger = None
			balance_sheet.total_capital_surplus = None
			balance_sheet.legal_reserve = None
			balance_sheet.special_reserve = None
			balance_sheet.total_unappropriated_retained_earnings_accumulated_deficit = None
			balance_sheet.total_retained_earnings = None
			balance_sheet.total_other_equity_interest = None
			balance_sheet.treasury_shares = None
			balance_sheet.total_equity_attributable_to_owners_of_parent = None
			balance_sheet.non_controlling_interests = None
			balance_sheet.total_equity = None
			balance_sheet.equivalent_issue_shares_of_advance_receipts_for_ordinary_share = None
			balance_sheet.number_of_shares_in_entity_held_by_entity_and_by_its_subsidiaries = None
			balance_sheet.modified_date = None

			# 公開資訊觀測站存放上市櫃公司綜合損益表的網址
			url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb03'
			values = {'encodeURIComponent': '1', 'step': '1', 'firstin': '1', 'off': '1',
						'keyword4': '', 'code1': '', 'TYPEK2': '', 'checkbtn': '',
						'queryName': 'co_id', 'TYPEK': 'all', 'isnew': 'false',
						'co_id': symbol, 'year': str(yr-1911), 'season': str(qtr).zfill(2)}
			url_data = urllib.urlencode(values)
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib2.Request(url, url_data, headers)

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
				season_balancesheet_datas = soup.find_all('td', attrs = {'style':'text-align:left;white-space:nowrap;'})
				busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
				# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
				while (busy_msg is not None):
					response.close()
					print("Server busy, Re-connect in 20 sec.")
					time.sleep(20)
					headers = {'User-Agent': 'Mozilla/4.0'}
					req = urllib2.Request(url, url_data, headers)
					try:
						response = urllib2.urlopen(req)
						print("Re-connect URL now!")
					except URLError, e:
						if hasattr(e, "reason"):
							print(symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
						elif hasattr(e, "code"):
							print(symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
					else:
						soup = BeautifulSoup(response, from_encoding = 'utf-8')
						season_balancesheet_datas = soup.find_all('td',
												attrs = {'style':'text-align:left;white-space:nowrap;'})
						busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})

				# 確認一切正常之後，才將網頁內容填入資料表(遇到名稱非常相似的，需增加字串長度檢查)
				for data in season_balancesheet_datas:
					if data.string != None:
						if r'現金及約當現金' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								# print('現金及約當現金:' + str(balance_sheet.total_cash_and_cash_equivalents))
						elif r'透過損益按公允價值衡量之金融資產－流動' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_current_financial_assets_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string)
								# print('透過損益按公允價值衡量之金融資產－流動:' + str(balance_sheet.total_current_financial_assets_at_fair_value_through_profit_or_loss))
						elif r'備供出售金融資產－流動淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.current_available_for_sale_financial_assets_net = string_to_decimal(next_data.string)
								# print('備供出售金融資產－流動淨額:' + str(balance_sheet.current_available_for_sale_financial_assets_net))
						elif r'持有至到期日金融資產－流動淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.current_held_to_maturity_financial_assets_net = string_to_decimal(next_data.string)
								# print('持有至到期日金融資產－流動淨額:' + str(balance_sheet.current_held_to_maturity_financial_assets_net))
						elif r'應收票據淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.notes_receivable_net = string_to_decimal(next_data.string)
								# print('應收票據淨額:' + str(balance_sheet.notes_receivable_net))
						elif r'應收帳款淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.accounts_receivable_net = string_to_decimal(next_data.string)
								# print('應收帳款淨額:' + str(balance_sheet.accounts_receivable_net))
						elif r'應收帳款－關係人淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.accounts_receivable_due_from_related_parties_net = string_to_decimal(next_data.string)
								# print('應收帳款－關係人淨額:' + str(balance_sheet.accounts_receivable_due_from_related_parties_net))
						elif r'其他應收款淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.other_receivables_net = string_to_decimal(next_data.string)
								# print('其他應收款淨額:' + str(balance_sheet.other_receivables_net))
						elif r'其他應收款－關係人淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.other_receivables_due_from_related_parties_net = string_to_decimal(next_data.string)
								# print('其他應收款－關係人淨額:' + str(balance_sheet.other_receivables_due_from_related_parties_net))
						elif r'存貨' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_inventories = string_to_decimal(next_data.string)
								# print('存貨:' + str(balance_sheet.total_inventories))
						elif r'預付款項' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_prepayments = string_to_decimal(next_data.string)
								# print('預付款項:' + str(balance_sheet.total_prepayments))
						elif r'其他流動資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_other_current_assets = string_to_decimal(next_data.string)
								# print('其他流動資產:' + str(balance_sheet.total_other_current_assets))
						elif r'流動資產合計' in data.string.encode('utf-8') and len(data.string.strip()) == 6:
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_current_assets = string_to_decimal(next_data.string)
								# print('流動資產合計:' + str(balance_sheet.total_current_assets))
						elif r'備供出售金融資產－非流動淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.non_current_available_for_sale_financial_assets_net = string_to_decimal(next_data.string)
								# print('備供出售金融資產－非流動淨額:' + str(balance_sheet.non_current_available_for_sale_financial_assets_net))
						elif r'持有至到期日金融資產－非流動淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.non_current_held_to_maturity_financial_assets_net = string_to_decimal(next_data.string)
								# print('持有至到期日金融資產－非流動淨額:' + str(balance_sheet.non_current_held_to_maturity_financial_assets_net))
						elif r'避險之衍生金融資產－非流動' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.derivative_non_current_financial_assets_for_hedging = string_to_decimal(next_data.string)
								# print('避險之衍生金融資產－非流動:' + str(balance_sheet.derivative_non_current_financial_assets_for_hedging))
						elif r'以成本衡量之金融資產－非流動淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.non_current_financial_assets_at_cost_net = string_to_decimal(next_data.string)
								# print('以成本衡量之金融資產－非流動淨額:' + str(balance_sheet.non_current_financial_assets_at_cost_net))
						elif r'採用權益法之投資淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.investments_accounted_for_using_equity_method_net = string_to_decimal(next_data.string)
								# print('採用權益法之投資淨額:' + str(balance_sheet.investments_accounted_for_using_equity_method_net))
						elif r'不動產、廠房及設備' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_property_plant_and_equipment = string_to_decimal(next_data.string)
								# print('不動產、廠房及設備:' + str(balance_sheet.total_property_plant_and_equipment))
						elif r'無形資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_intangible_assets = string_to_decimal(next_data.string)
								# print('無形資產:' + str(balance_sheet.total_intangible_assets))
						elif r'遞延所得稅資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.deferred_tax_assets = string_to_decimal(next_data.string)
								# print('遞延所得稅資產:' + str(balance_sheet.deferred_tax_assets))
						elif r'其他非流動資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_other_non_current_assets = string_to_decimal(next_data.string)
								# print('其他非流動資產:' + str(balance_sheet.total_other_non_current_assets))
						elif r'非流動資產合計' in data.string.encode('utf-8') and len(data.string.strip()) == 7:
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_non_current_assets = string_to_decimal(next_data.string)
								# print('非流動資產合計:' + str(balance_sheet.total_non_current_assets))
						elif r'資產總額' in data.string.encode('utf-8') or (r'資產合計' in data.string.encode('utf-8') and len(data.string.strip()) == 4):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_assets = string_to_decimal(next_data.string)
								# print('資產總額:' + str(balance_sheet.total_assets))
						elif r'短期借款' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_short_term_borrowings = string_to_decimal(next_data.string)
								# print('短期借款:' + str(balance_sheet.total_short_term_borrowings))
						elif r'透過損益按公允價值衡量之金融負債－流動' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_current_financial_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string)
								# print('透過損益按公允價值衡量之金融負債－流動:' + str(balance_sheet.total_current_financial_liabilities_at_fair_value_through_profit_or_loss))
						elif r'應付短期票券' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								# print('應付短期票券:' + str(balance_sheet.total_short_term_notes_and_bills_payable))
						elif r'應付帳款' in data.string.encode('utf-8') and len(data.string.strip()) == 4:
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_accounts_payable = string_to_decimal(next_data.string)
								# print('應付帳款:' + str(balance_sheet.total_accounts_payable))
						elif r'應付帳款－關係人' in data.string.encode('utf-8') and len(data.string.strip()) == 8:
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_accounts_payable_to_related_parties = string_to_decimal(next_data.string)
								# print('應付帳款－關係人:' + str(balance_sheet.total_accounts_payable_to_related_parties))
						elif r'其他應付款' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_other_payables = string_to_decimal(next_data.string)
								# print('其他應付款:' + str(balance_sheet.total_other_payables))
						elif r'當期所得稅負債' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.current_tax_liabilities = string_to_decimal(next_data.string)
								# print('當期所得稅負債:' + str(balance_sheet.current_tax_liabilities))
						elif r'負債準備－流動' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_current_provisions = string_to_decimal(next_data.string)
								# print('負債準備－流動:' + str(balance_sheet.total_current_provisions))
						elif r'其他流動負債' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_other_current_liabilities = string_to_decimal(next_data.string)
								# print('其他流動負債:' + str(balance_sheet.total_other_current_liabilities))
						elif r'流動負債合計' in data.string.encode('utf-8') and len(data.string.strip()) == 6:
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_current_liabilities = string_to_decimal(next_data.string)
								# print('流動負債合計:' + str(balance_sheet.total_current_liabilities))
						elif r'應付公司債' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_bonds_payable = string_to_decimal(next_data.string)
								# print('應付公司債:' + str(balance_sheet.total_bonds_payable))
						elif r'長期借款' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_long_borrowings = string_to_decimal(next_data.string)
								# print('長期借款:' + str(balance_sheet.total_long_borrowings))
						elif r'負債準備－非流動' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_non_current_provisions = string_to_decimal(next_data.string)
								# print('負債準備－非流動:' + str(balance_sheet.total_non_current_provisions))
						elif r'遞延所得稅負債' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_deferred_tax_liabilities = string_to_decimal(next_data.string)
								# print('遞延所得稅負債:' + str(balance_sheet.total_deferred_tax_liabilities))
						elif r'其他非流動負債' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_other_non_current_liabilities = string_to_decimal(next_data.string)
								# print('其他非流動負債:' + str(balance_sheet.total_other_non_current_liabilities))
						elif r'非流動負債合計' in data.string.encode('utf-8') and len(data.string.strip()) == 7:
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_non_current_liabilities = string_to_decimal(next_data.string)
								# print('非流動負債合計:' + str(balance_sheet.total_non_current_liabilities))
						elif r'負債總額' in data.string.encode('utf-8') or (r'負債合計' in data.string.encode('utf-8') and len(data.string.strip()) == 4):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_liabilities = string_to_decimal(next_data.string)
								# print('負債總額:' + str(balance_sheet.total_liabilities))
						elif r'普通股股本' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.ordinary_share = string_to_decimal(next_data.string)
								# print('普通股股本:' + str(balance_sheet.ordinary_share))
						elif r'股本合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_capital_stock = string_to_decimal(next_data.string)
								# print('股本合計:' + str(balance_sheet.total_capital_stock))
						elif r'資本公積－發行溢價' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_capital_surplus_additional_paid_in_capital = string_to_decimal(next_data.string)
								# print('資本公積－發行溢價:' + str(balance_sheet.total_capital_surplus_additional_paid_in_capital))
						elif r'資本公積－取得或處分子公司股權價格與帳面價值差額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.capital_surplus_difference_between_consideration_and_carrying_amount_of_subsidiaries_acquired_or_disposed = string_to_decimal(next_data.string)
								# print('資本公積－取得或處分子公司股權價格與帳面價值差額:' + str(balance_sheet.capital_surplus_difference_between_consideration_and_carrying_amount_of_subsidiaries_acquired_or_disposed))
						elif r'資本公積－受贈資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_capital_surplus_donated_assets_received = string_to_decimal(next_data.string)
								# print('資本公積－受贈資產:' + str(balance_sheet.total_capital_surplus_donated_assets_received))
						elif r'資本公積－採用權益法認列關聯企業及合資股權淨值之變動數' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.capital_surplus_changes_in_equity_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								# print('資本公積－採用權益法認列關聯企業及合資股權淨值之變動數:' + str(balance_sheet.capital_surplus_changes_in_equity_of_associates_and_joint_ventures_accounted_for_using_equity_method))
						elif r'資本公積－合併溢額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.capital_surplus_net_assets_from_merger = string_to_decimal(next_data.string)
								# print('資本公積－合併溢額:' + str(balance_sheet.capital_surplus_net_assets_from_merger))
						elif r'資本公積合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_capital_surplus = string_to_decimal(next_data.string)
								# print('資本公積合計:' + str(balance_sheet.total_capital_surplus))
						elif r'法定盈餘公積' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.legal_reserve = string_to_decimal(next_data.string)
								# print('法定盈餘公積:' + str(balance_sheet.legal_reserve))
						elif r'特別盈餘公積' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.special_reserve = string_to_decimal(next_data.string)
								# print('特別盈餘公積:' + str(balance_sheet.special_reserve))
						elif r'未分配盈餘（或待彌補虧損）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_unappropriated_retained_earnings_accumulated_deficit = string_to_decimal(next_data.string)
								# print('未分配盈餘（或待彌補虧損）:' + str(balance_sheet.total_unappropriated_retained_earnings_accumulated_deficit))
						elif r'保留盈餘合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_retained_earnings = string_to_decimal(next_data.string)
								# print('保留盈餘合計:' + str(balance_sheet.total_retained_earnings))
						elif r'其他權益合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_other_equity_interest = string_to_decimal(next_data.string)
								# print('其他權益合計:' + str(balance_sheet.total_other_equity_interest))
						elif r'庫藏股票' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.treasury_shares = string_to_decimal(next_data.string)
								# print('庫藏股票:' + str(balance_sheet.treasury_shares))
						elif r'歸屬於母公司業主之權益合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_equity_attributable_to_owners_of_parent = string_to_decimal(next_data.string)
								# print('歸屬於母公司業主之權益合計:' + str(balance_sheet.total_equity_attributable_to_owners_of_parent))
						elif r'非控制權益' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.non_controlling_interests = string_to_decimal(next_data.string)
								# print('非控制權益:' + str(balance_sheet.non_controlling_interests))
						elif r'權益總額' in data.string.encode('utf-8') or (r'權益合計' in data.string.encode('utf-8') and len(data.string.strip()) == 4):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.total_equity = string_to_decimal(next_data.string)
								# print('權益總額:' + str(balance_sheet.total_equity))
						elif r'預收股款（權益項下）之約當發行股數（單位：股）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.equivalent_issue_shares_of_advance_receipts_for_ordinary_share = string_to_decimal(next_data.string)
								# print('預收股款（權益項下）之約當發行股數（單位：股）:' + str(balance_sheet.equivalent_issue_shares_of_advance_receipts_for_ordinary_share))
						elif r'母公司暨子公司所持有之母公司庫藏股股數（單位：股）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								balance_sheet.number_of_shares_in_entity_held_by_entity_and_by_its_subsidiaries = string_to_decimal(next_data.string)
								# print('母公司暨子公司所持有之母公司庫藏股股數（單位：股）:' + str(balance_sheet.number_of_shares_in_entity_held_by_entity_and_by_its_subsidiaries))

				response.close()
				# 確定有抓到權益總額的值，才將該檔股票資料寫入資料表中
				if balance_sheet.total_equity is not None:
					balance_sheet.save()
					print(symbol + " updated.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ") @ " + str(datetime.now()))
				else:
					print(symbol + " no data.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")
	
	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name":"資產負債表(季)"})

# 綜合損益表（季）
def season_income_statement(request):

	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stockfins_seasonincomestatement')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	# # 輸入西元年(時間參數改由最外層控制)
	# yr = 2014 
	# season = [2]

	start_time = datetime.now()
	stockID_updated = get_stockID_updated(request)

	for qtr in season:
		income_statement = SeasonIncomeStatement()
		count = 0
		stocks = StockID.objects.all()[count:]
		countAll = stocks.count() # 計算全部需要更新的股票檔數

		if qtr == 4:
			# 若是Q4，則先將可能存在的Q3,Q2,Q1物件取出
			incomeStatementsSeason1 = SeasonIncomeStatement.objects.filter(year=yr, season="Q1")
			incomeStatementsSeason2 = SeasonIncomeStatement.objects.filter(year=yr, season="Q2")
			incomeStatementsSeason3 = SeasonIncomeStatement.objects.filter(year=yr, season="Q3")
			
		for stock in stocks:
			symbol = stock.symbol
			mkt = stock.market
			count = count + 1
			# STEP1.跳過金融股
			if symbol[:2] == "28":
				continue
			# STEP2.檢查資料是否已經存在資料庫，如果「是」，就跳過此檔不更新，以節省時間
			id_test_exist = str(yr) + 'Q' + str(qtr) + '-' + symbol
			if SeasonIncomeStatement.objects.filter(ID=id_test_exist):
				print(symbol + u"資料已存在資料庫.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")
				continue
			# STEP3.檢查該檔股票的財報是否已經在更新清單裡面，如果有才進行連線更新，沒有的話就跳過
			if symbol not in stockID_updated:
				print(symbol + u"網站資料尚未更新.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")
				continue
			# 先宣告所有報表項目
			income_statement.ID = str(yr) + 'Q' + str(qtr) + '-' + symbol
			income_statement.symbol = symbol
			income_statement.year = yr
			income_statement.season = 'Q' + str(qtr)
			income_statement.date = str(yr) + 'Q' + str(qtr)
			income_statement.net_sales_revenue = None
			income_statement.total_service_revenue = None
			income_statement.total_operating_revenue = None
			income_statement.total_cost_of_sales = None
			income_statement.total_cost_of_services = None
			income_statement.total_operating_costs = None
			income_statement.gross_profit_loss_from_operations = None
			income_statement.gross_profit_loss_from_operations_net = None
			income_statement.total_selling_expenses = None
			income_statement.total_administrative_expenses = None
			income_statement.total_research_and_development_expenses = None
			income_statement.total_operating_expenses = None
			income_statement.net_operating_income_loss = None
			income_statement.total_other_income = None
			income_statement.other_gains_and_losses_net = None
			income_statement.finance_costs_net = None
			income_statement.total_non_operating_income_and_expenses = None
			income_statement.profit_loss_from_continuing_operations_before_tax = None
			income_statement.total_tax_expense_income = None
			income_statement.profit_loss_from_continuing_operations = None
			income_statement.profit_loss = None
			income_statement.exchange_differences_on_translation = None
			income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = None
			income_statement.other_comprehensive_income_net = None
			income_statement.total_comprehensive_income = None
			income_statement.profit_loss_attributable_to_owners_of_parent = None
			income_statement.profit_loss_attributable_to_non_controlling_interests = None
			income_statement.comprehensive_income_attributable_to_owners_of_parent = None
			income_statement.comprehensive_income_attributable_to_non_controlling_interests = None
			income_statement.total_basic_earnings_per_share = None
			income_statement.total_diluted_earnings_per_share = None
			income_statement.total_operating_revenue_yoy = None

			id_filter = str(yr - 1) + "Q" + str(qtr) + "-" + symbol
			try:
				SeasonIncomeStatement.objects.get(ID=id_filter)
			except:
				total_operating_revenue_pre = None
			else:
				total_operating_revenue_pre = SeasonIncomeStatement.objects.filter(ID=id_filter).values_list("total_operating_revenue", flat=True)[0]

			symbolSeason1 = None
			symbolSeason2 = None
			symbolSeason3 = None
			has_3_PrevSeasons = False
			has_2_PrevSeasons = False
			has_1_PrevSeasons = False

			# 抓Q4資料之前，先將該檔股票Q3,Q2,Q1的資料取出(不一定都有)，並依存在情況定義has_n_PreSeasons為True
			if qtr == 4:
				if incomeStatementsSeason1:
					if incomeStatementsSeason1.filter(symbol=symbol):
						symbolSeason1 = incomeStatementsSeason1.get(symbol=symbol)
				if incomeStatementsSeason2:
					if incomeStatementsSeason2.filter(symbol=symbol):
						symbolSeason2 = incomeStatementsSeason2.get(symbol=symbol)
				if incomeStatementsSeason3:
					if incomeStatementsSeason3.filter(symbol=symbol):
						symbolSeason3 = incomeStatementsSeason3.get(symbol=symbol)
				if symbolSeason1 and symbolSeason2 and symbolSeason3:
					has_3_PrevSeasons = True
				elif symbolSeason2 and symbolSeason3:
					has_2_PrevSeasons = True
				elif symbolSeason3:
					has_1_PrevSeasons = True

			# 公開資訊觀測站存放上市櫃公司綜合損益表的網址
			url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb04'
			values = {'encodeURIComponent': '1', 'step': '1', 'firstin': '1', 'off': '1',
						'keyword4': '', 'code1': '', 'TYPEK2': '', 'checkbtn': '',
						'queryName': 'co_id', 'TYPEK': 'all', 'isnew': 'false',
						'co_id': symbol, 'year': str(yr-1911), 'season': str(qtr).zfill(2)}
			url_data = urllib.urlencode(values)
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib2.Request(url, url_data, headers)

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
				season_income_datas = soup.find_all('td', attrs = {'style':'text-align:left;white-space:nowrap;'})
				busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
				# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
				while (busy_msg is not None):
					response.close()
					print("Server busy, Re-connect in 20 sec.")
					time.sleep(20)
					headers = {'User-Agent': 'Mozilla/4.0'}
					req = urllib2.Request(url, url_data, headers)
					try:
						response = urllib2.urlopen(req)
						print("Re-connect URL now!")
					except URLError, e:
						if hasattr(e, "reason"):
							print(symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
						elif hasattr(e, "code"):
							print(symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
					else:
						soup = BeautifulSoup(response, from_encoding = 'utf-8')
						season_income_datas = soup.find_all('td', attrs = {'style':'text-align:left;white-space:nowrap;'})
						busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})

				# 確認一切正常之後，才將網頁內容填入資料表
				for data in season_income_datas:
					if data.string != None:
						if r'銷貨收入淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.net_sales_revenue = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.net_sales_revenue and symbolSeason2.net_sales_revenue and symbolSeason3.net_sales_revenue:
									income_statement.net_sales_revenue = string_to_decimal(next_data.string) - symbolSeason1.net_sales_revenue - symbolSeason2.net_sales_revenue - symbolSeason3.net_sales_revenue
								elif has_2_PrevSeasons and symbolSeason2.net_sales_revenue and symbolSeason3.net_sales_revenue:
									income_statement.net_sales_revenue = string_to_decimal(next_data.string) - symbolSeason2.net_sales_revenue - symbolSeason3.net_sales_revenue
								elif has_1_PrevSeasons and symbolSeason3.net_sales_revenue:
									income_statement.net_sales_revenue = string_to_decimal(next_data.string) - symbolSeason3.net_sales_revenue
								else:
									income_statement.net_sales_revenue = string_to_decimal(next_data.string)
								# print('銷貨收入淨額:' + str(income_statement.net_sales_revenue))
						elif r'勞務收入' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_service_revenue = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_service_revenue and symbolSeason2.total_service_revenue and symbolSeason3.total_service_revenue:
									income_statement.total_service_revenue = string_to_decimal(next_data.string) - symbolSeason1.total_service_revenue - symbolSeason2.total_service_revenue - symbolSeason3.total_service_revenue
								elif has_2_PrevSeasons and symbolSeason2.total_service_revenue and symbolSeason3.total_service_revenue:
									income_statement.total_service_revenue = string_to_decimal(next_data.string) - symbolSeason2.total_service_revenue - symbolSeason3.total_service_revenue
								elif has_1_PrevSeasons and symbolSeason3.total_service_revenue:
									income_statement.total_service_revenue = string_to_decimal(next_data.string) - symbolSeason3.total_service_revenue
								else:
									income_statement.total_service_revenue = string_to_decimal(next_data.string)
								# print('勞務收入:' + str(income_statement.total_service_revenue))
						elif r'營業收入合計' in data.string.encode('utf-8') or r'收入合計' in data.string.encode('utf-8') or r'收益合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_operating_revenue = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_operating_revenue and symbolSeason2.total_operating_revenue and symbolSeason3.total_operating_revenue:
									income_statement.total_operating_revenue = string_to_decimal(next_data.string) - symbolSeason1.total_operating_revenue - symbolSeason2.total_operating_revenue - symbolSeason3.total_operating_revenue
								elif has_2_PrevSeasons and symbolSeason2.total_operating_revenue and symbolSeason3.total_operating_revenue:
									income_statement.total_operating_revenue = string_to_decimal(next_data.string) - symbolSeason2.total_operating_revenue - symbolSeason3.total_operating_revenue
								elif has_1_PrevSeasons and symbolSeason3.total_operating_revenue:
									income_statement.total_operating_revenue = string_to_decimal(next_data.string) - symbolSeason3.total_operating_revenue
								else:
									income_statement.total_operating_revenue = string_to_decimal(next_data.string)
								# print('營業收入合計:' + str(income_statement.total_operating_revenue))
								# 以下為計算營收年增率，如果是第1,2,3季就直接根據網頁資料相除得到年增率，但若是第4季，則回資料庫找有無前一年數字，有的話就計算年增率，沒有就給0
								if qtr != 4 and data.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string is not None:
									total_operating_revenue_pre = string_to_decimal(data.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string)									
								if total_operating_revenue_pre != None and total_operating_revenue_pre != 0:
									income_statement.total_operating_revenue_yoy = (income_statement.total_operating_revenue / total_operating_revenue_pre - 1) * 100
								else:
									income_statement.total_operating_revenue_yoy = 0
								# print('營收年增率:' + str(income_statement.total_operating_revenue_yoy))
						elif r'銷貨成本' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_cost_of_sales = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_cost_of_sales and symbolSeason2.total_cost_of_sales and symbolSeason3.total_cost_of_sales:
									income_statement.total_cost_of_sales = string_to_decimal(next_data.string) - symbolSeason1.total_cost_of_sales - symbolSeason2.total_cost_of_sales - symbolSeason3.total_cost_of_sales
								elif has_2_PrevSeasons and symbolSeason2.total_cost_of_sales and symbolSeason3.total_cost_of_sales:
									income_statement.total_cost_of_sales = string_to_decimal(next_data.string) - symbolSeason2.total_cost_of_sales - symbolSeason3.total_cost_of_sales
								elif has_1_PrevSeasons and symbolSeason3.total_cost_of_sales:
									income_statement.total_cost_of_sales = string_to_decimal(next_data.string) - symbolSeason3.total_cost_of_sales
								else:
									income_statement.total_cost_of_sales = string_to_decimal(next_data.string)
								# print('銷貨成本:' + str(income_statement.total_cost_of_sales))
						elif r'勞務成本' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_cost_of_services = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_cost_of_services and symbolSeason2.total_cost_of_services and symbolSeason3.total_cost_of_services:
									income_statement.total_cost_of_services = string_to_decimal(next_data.string) - symbolSeason1.total_cost_of_services - symbolSeason2.total_cost_of_services - symbolSeason3.total_cost_of_services
								elif has_2_PrevSeasons and symbolSeason2.total_cost_of_services and symbolSeason3.total_cost_of_services:
									income_statement.total_cost_of_services = string_to_decimal(next_data.string) - symbolSeason2.total_cost_of_services - symbolSeason3.total_cost_of_services
								elif has_1_PrevSeasons and symbolSeason3.total_cost_of_services:
									income_statement.total_cost_of_services = string_to_decimal(next_data.string) - symbolSeason3.total_cost_of_services
								else:
									income_statement.total_cost_of_services = string_to_decimal(next_data.string)
								# print('勞務成本:' + str(income_statement.total_cost_of_services))
						elif r'營業成本合計' in data.string.encode('utf-8') or r'支出合計' in data.string.encode('utf-8') or r'支出及費用合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_operating_costs = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_operating_costs and symbolSeason2.total_operating_costs and symbolSeason3.total_operating_costs:
									income_statement.total_operating_costs = string_to_decimal(next_data.string) - symbolSeason1.total_operating_costs - symbolSeason2.total_operating_costs - symbolSeason3.total_operating_costs
								elif has_2_PrevSeasons and symbolSeason2.total_operating_costs and symbolSeason3.total_operating_costs:
									income_statement.total_operating_costs = string_to_decimal(next_data.string) - symbolSeason2.total_operating_costs - symbolSeason3.total_operating_costs
								elif has_1_PrevSeasons and symbolSeason3.total_operating_costs:
									income_statement.total_operating_costs = string_to_decimal(next_data.string) - symbolSeason3.total_operating_costs
								else:
									income_statement.total_operating_costs = string_to_decimal(next_data.string)
								# print('營業成本合計:' + str(income_statement.total_operating_costs))
						elif r'營業毛利（毛損）' == data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.gross_profit_loss_from_operations = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.gross_profit_loss_from_operations and symbolSeason2.gross_profit_loss_from_operations and symbolSeason3.gross_profit_loss_from_operations:
									income_statement.gross_profit_loss_from_operations = string_to_decimal(next_data.string) - symbolSeason1.gross_profit_loss_from_operations - symbolSeason2.gross_profit_loss_from_operations - symbolSeason3.gross_profit_loss_from_operations
								elif has_2_PrevSeasons and symbolSeason2.gross_profit_loss_from_operations and symbolSeason3.gross_profit_loss_from_operations:
									income_statement.gross_profit_loss_from_operations = string_to_decimal(next_data.string) - symbolSeason2.gross_profit_loss_from_operations - symbolSeason3.gross_profit_loss_from_operations
								elif has_1_PrevSeasons and symbolSeason3.gross_profit_loss_from_operations:
									income_statement.gross_profit_loss_from_operations = string_to_decimal(next_data.string) - symbolSeason3.gross_profit_loss_from_operations
								else:
									income_statement.gross_profit_loss_from_operations = string_to_decimal(next_data.string)
								# print('營業毛利（毛損）:' + str(income_statement.gross_profit_loss_from_operations))
						elif r'營業毛利（毛損）淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.gross_profit_loss_from_operations_net = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.gross_profit_loss_from_operations_net and symbolSeason2.gross_profit_loss_from_operations_net and symbolSeason3.gross_profit_loss_from_operations_net:
									income_statement.gross_profit_loss_from_operations_net = string_to_decimal(next_data.string) - symbolSeason1.gross_profit_loss_from_operations_net - symbolSeason2.gross_profit_loss_from_operations_net - symbolSeason3.gross_profit_loss_from_operations_net
								elif has_2_PrevSeasons and symbolSeason2.gross_profit_loss_from_operations_net and symbolSeason3.gross_profit_loss_from_operations_net:
									income_statement.gross_profit_loss_from_operations_net = string_to_decimal(next_data.string) - symbolSeason2.gross_profit_loss_from_operations_net - symbolSeason3.gross_profit_loss_from_operations_net
								elif has_1_PrevSeasons and symbolSeason3.gross_profit_loss_from_operations_net:
									income_statement.gross_profit_loss_from_operations_net = string_to_decimal(next_data.string) - symbolSeason3.gross_profit_loss_from_operations_net
								else:
									income_statement.gross_profit_loss_from_operations_net = string_to_decimal(next_data.string)
								# print('營業毛利（毛損）淨額:' + str(income_statement.gross_profit_loss_from_operations_net))
						elif r'推銷費用' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_selling_expenses = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_selling_expenses and symbolSeason2.total_selling_expenses and symbolSeason3.total_selling_expenses:
									income_statement.total_selling_expenses = string_to_decimal(next_data.string) - symbolSeason1.total_selling_expenses - symbolSeason2.total_selling_expenses - symbolSeason3.total_selling_expenses
								elif has_2_PrevSeasons and symbolSeason2.total_selling_expenses and symbolSeason3.total_selling_expenses:
									income_statement.total_selling_expenses = string_to_decimal(next_data.string) - symbolSeason2.total_selling_expenses - symbolSeason3.total_selling_expenses
								elif has_1_PrevSeasons and symbolSeason3.total_selling_expenses:
									income_statement.total_selling_expenses = string_to_decimal(next_data.string) - symbolSeason3.total_selling_expenses
								else:
									income_statement.total_selling_expenses = string_to_decimal(next_data.string)
								# print('推銷費用:' + str(income_statement.total_selling_expenses))
						elif r'管理費用' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_administrative_expenses = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_administrative_expenses and symbolSeason2.total_administrative_expenses and symbolSeason3.total_administrative_expenses:
									income_statement.total_administrative_expenses = string_to_decimal(next_data.string) - symbolSeason1.total_administrative_expenses - symbolSeason2.total_administrative_expenses - symbolSeason3.total_administrative_expenses
								elif has_2_PrevSeasons and symbolSeason2.total_administrative_expenses and symbolSeason3.total_administrative_expenses:
									income_statement.total_administrative_expenses = string_to_decimal(next_data.string) - symbolSeason2.total_administrative_expenses - symbolSeason3.total_administrative_expenses
								elif has_1_PrevSeasons and symbolSeason3.total_administrative_expenses:
									income_statement.total_administrative_expenses = string_to_decimal(next_data.string) - symbolSeason3.total_administrative_expenses
								else:
									income_statement.total_administrative_expenses = string_to_decimal(next_data.string)
								# print('管理費用:' + str(income_statement.total_administrative_expenses))
						elif r'研究發展費用' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_research_and_development_expenses = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_research_and_development_expenses and symbolSeason2.total_research_and_development_expenses and symbolSeason3.total_research_and_development_expenses:
									income_statement.total_research_and_development_expenses = string_to_decimal(next_data.string) - symbolSeason1.total_research_and_development_expenses - symbolSeason2.total_research_and_development_expenses - symbolSeason3.total_research_and_development_expenses
								elif has_2_PrevSeasons and symbolSeason2.total_research_and_development_expenses and symbolSeason3.total_research_and_development_expenses:
									income_statement.total_research_and_development_expenses = string_to_decimal(next_data.string) - symbolSeason2.total_research_and_development_expenses - symbolSeason3.total_research_and_development_expenses
								elif has_1_PrevSeasons and symbolSeason3.total_research_and_development_expenses:
									income_statement.total_research_and_development_expenses = string_to_decimal(next_data.string) - symbolSeason3.total_research_and_development_expenses
								else:
									income_statement.total_research_and_development_expenses = string_to_decimal(next_data.string)
								# print('研究發展費用:' + str(income_statement.total_research_and_development_expenses))
						elif r'營業費用合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_operating_expenses = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_operating_expenses and symbolSeason2.total_operating_expenses and symbolSeason3.total_operating_expenses:
									income_statement.total_operating_expenses = string_to_decimal(next_data.string) - symbolSeason1.total_operating_expenses - symbolSeason2.total_operating_expenses - symbolSeason3.total_operating_expenses
								elif has_2_PrevSeasons and symbolSeason2.total_operating_expenses and symbolSeason3.total_operating_expenses:
									income_statement.total_operating_expenses = string_to_decimal(next_data.string) - symbolSeason2.total_operating_expenses - symbolSeason3.total_operating_expenses
								elif has_1_PrevSeasons and symbolSeason3.total_operating_expenses:
									income_statement.total_operating_expenses = string_to_decimal(next_data.string) - symbolSeason3.total_operating_expenses
								else:
									income_statement.total_operating_expenses = string_to_decimal(next_data.string)
								# print('營業費用合計:' + str(income_statement.total_operating_expenses))
						elif r'營業利益（損失）' in data.string.encode('utf-8') or r'營業利益' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.net_operating_income_loss = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.net_operating_income_loss and symbolSeason2.net_operating_income_loss and symbolSeason3.net_operating_income_loss:
									income_statement.net_operating_income_loss = string_to_decimal(next_data.string) - symbolSeason1.net_operating_income_loss - symbolSeason2.net_operating_income_loss - symbolSeason3.net_operating_income_loss
								elif has_2_PrevSeasons and symbolSeason2.net_operating_income_loss and symbolSeason3.net_operating_income_loss:
									income_statement.net_operating_income_loss = string_to_decimal(next_data.string) - symbolSeason2.net_operating_income_loss - symbolSeason3.net_operating_income_loss
								elif has_1_PrevSeasons and symbolSeason3.net_operating_income_loss:
									income_statement.net_operating_income_loss = string_to_decimal(next_data.string) - symbolSeason3.net_operating_income_loss
								else:
									income_statement.net_operating_income_loss = string_to_decimal(next_data.string)
								# print('營業利益（損失）:' + str(income_statement.net_operating_income_loss))
						elif r'其他收入' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_other_income = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_other_income and symbolSeason2.total_other_income and symbolSeason3.total_other_income:
									income_statement.total_other_income = string_to_decimal(next_data.string) - symbolSeason1.total_other_income - symbolSeason2.total_other_income - symbolSeason3.total_other_income
								elif has_2_PrevSeasons and symbolSeason2.total_other_income and symbolSeason3.total_other_income:
									income_statement.total_other_income = string_to_decimal(next_data.string) - symbolSeason2.total_other_income - symbolSeason3.total_other_income
								elif has_1_PrevSeasons and symbolSeason3.total_other_income:
									income_statement.total_other_income = string_to_decimal(next_data.string) - symbolSeason3.total_other_income
								else:
									income_statement.total_other_income = string_to_decimal(next_data.string)
								# print('其他收入:' + str(income_statement.total_other_income))
						elif r'其他利益及損失淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.other_gains_and_losses_net = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.other_gains_and_losses_net and symbolSeason2.other_gains_and_losses_net and symbolSeason3.other_gains_and_losses_net:
									income_statement.other_gains_and_losses_net = string_to_decimal(next_data.string) - symbolSeason1.other_gains_and_losses_net - symbolSeason2.other_gains_and_losses_net - symbolSeason3.other_gains_and_losses_net
								elif has_2_PrevSeasons and symbolSeason2.other_gains_and_losses_net and symbolSeason3.other_gains_and_losses_net:
									income_statement.other_gains_and_losses_net = string_to_decimal(next_data.string) - symbolSeason2.other_gains_and_losses_net - symbolSeason3.other_gains_and_losses_net
								elif has_1_PrevSeasons and symbolSeason3.other_gains_and_losses_net:
									income_statement.other_gains_and_losses_net = string_to_decimal(next_data.string) - symbolSeason3.other_gains_and_losses_net
								else:
									income_statement.other_gains_and_losses_net = string_to_decimal(next_data.string)
								# print('其他利益及損失淨額:' + str(income_statement.other_gains_and_losses_net))
						elif r'財務成本淨額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.finance_costs_net = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.finance_costs_net and symbolSeason2.finance_costs_net and symbolSeason3.finance_costs_net:
									income_statement.finance_costs_net = string_to_decimal(next_data.string) - symbolSeason1.finance_costs_net - symbolSeason2.finance_costs_net - symbolSeason3.finance_costs_net
								elif has_2_PrevSeasons and symbolSeason2.finance_costs_net and symbolSeason3.finance_costs_net:
									income_statement.finance_costs_net = string_to_decimal(next_data.string) - symbolSeason2.finance_costs_net - symbolSeason3.finance_costs_net
								elif has_1_PrevSeasons and symbolSeason3.finance_costs_net:
									income_statement.finance_costs_net = string_to_decimal(next_data.string) - symbolSeason3.finance_costs_net
								else:
									income_statement.finance_costs_net = string_to_decimal(next_data.string)
								# print('財務成本淨額:' + str(income_statement.finance_costs_net))
						elif r'營業外收入及支出合計' in data.string.encode('utf-8') or r'營業外損益合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_non_operating_income_and_expenses = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_non_operating_income_and_expenses and symbolSeason2.total_non_operating_income_and_expenses and symbolSeason3.total_non_operating_income_and_expenses:
									income_statement.total_non_operating_income_and_expenses = string_to_decimal(next_data.string) - symbolSeason1.total_non_operating_income_and_expenses - symbolSeason2.total_non_operating_income_and_expenses - symbolSeason3.total_non_operating_income_and_expenses
								elif has_2_PrevSeasons and symbolSeason2.total_non_operating_income_and_expenses and symbolSeason3.total_non_operating_income_and_expenses:
									income_statement.total_non_operating_income_and_expenses = string_to_decimal(next_data.string) - symbolSeason2.total_non_operating_income_and_expenses - symbolSeason3.total_non_operating_income_and_expenses
								elif has_1_PrevSeasons and symbolSeason3.total_non_operating_income_and_expenses:
									income_statement.total_non_operating_income_and_expenses = string_to_decimal(next_data.string) - symbolSeason3.total_non_operating_income_and_expenses
								else:
									income_statement.total_non_operating_income_and_expenses = string_to_decimal(next_data.string)
								# print('營業外收入及支出合計:' + str(income_statement.total_non_operating_income_and_expenses))
						elif r'稅前淨利（淨損）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.profit_loss_from_continuing_operations_before_tax and symbolSeason2.profit_loss_from_continuing_operations_before_tax and symbolSeason3.profit_loss_from_continuing_operations_before_tax:
									income_statement.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_from_continuing_operations_before_tax - symbolSeason2.profit_loss_from_continuing_operations_before_tax - symbolSeason3.profit_loss_from_continuing_operations_before_tax
								elif has_2_PrevSeasons and symbolSeason2.profit_loss_from_continuing_operations_before_tax and symbolSeason3.profit_loss_from_continuing_operations_before_tax:
									income_statement.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason2.profit_loss_from_continuing_operations_before_tax - symbolSeason3.profit_loss_from_continuing_operations_before_tax
								elif has_1_PrevSeasons and symbolSeason3.profit_loss_from_continuing_operations_before_tax:
									income_statement.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason3.profit_loss_from_continuing_operations_before_tax
								else:
									income_statement.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string)
								# print('稅前淨利（淨損）:' + str(income_statement.profit_loss_from_continuing_operations_before_tax))
						elif r'所得稅費用（利益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_tax_expense_income = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_tax_expense_income and symbolSeason2.total_tax_expense_income and symbolSeason3.total_tax_expense_income:
									income_statement.total_tax_expense_income = string_to_decimal(next_data.string) - symbolSeason1.total_tax_expense_income - symbolSeason2.total_tax_expense_income - symbolSeason3.total_tax_expense_income
								elif has_2_PrevSeasons and symbolSeason2.total_tax_expense_income and symbolSeason3.total_tax_expense_income:
									income_statement.total_tax_expense_income = string_to_decimal(next_data.string) - symbolSeason2.total_tax_expense_income - symbolSeason3.total_tax_expense_income
								elif has_1_PrevSeasons and symbolSeason3.total_tax_expense_income:
									income_statement.total_tax_expense_income = string_to_decimal(next_data.string) - symbolSeason3.total_tax_expense_income
								else:
									income_statement.total_tax_expense_income = string_to_decimal(next_data.string)
								# print('所得稅費用（利益）合計:' + str(income_statement.total_tax_expense_income))
						elif r'繼續營業單位本期淨利（淨損）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.profit_loss_from_continuing_operations = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.profit_loss_from_continuing_operations and symbolSeason2.profit_loss_from_continuing_operations and symbolSeason3.profit_loss_from_continuing_operations:
									income_statement.profit_loss_from_continuing_operations = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_from_continuing_operations - symbolSeason2.profit_loss_from_continuing_operations - symbolSeason3.profit_loss_from_continuing_operations
								elif has_2_PrevSeasons and symbolSeason2.profit_loss_from_continuing_operations and symbolSeason3.profit_loss_from_continuing_operations:
									income_statement.profit_loss_from_continuing_operations = string_to_decimal(next_data.string) - symbolSeason2.profit_loss_from_continuing_operations - symbolSeason3.profit_loss_from_continuing_operations
								elif has_1_PrevSeasons and symbolSeason3.profit_loss_from_continuing_operations:
									income_statement.profit_loss_from_continuing_operations = string_to_decimal(next_data.string) - symbolSeason3.profit_loss_from_continuing_operations
								else:
									income_statement.profit_loss_from_continuing_operations = string_to_decimal(next_data.string)
								# print('繼續營業單位本期淨利（淨損）:' + str(income_statement.profit_loss_from_continuing_operations))
						elif r'本期淨利（淨損）' == data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.profit_loss = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.profit_loss and symbolSeason2.profit_loss and symbolSeason3.profit_loss:
									income_statement.profit_loss = string_to_decimal(next_data.string) - symbolSeason1.profit_loss - symbolSeason2.profit_loss - symbolSeason3.profit_loss
								elif has_2_PrevSeasons and symbolSeason2.profit_loss and symbolSeason3.profit_loss:
									income_statement.profit_loss = string_to_decimal(next_data.string) - symbolSeason2.profit_loss - symbolSeason3.profit_loss
								elif has_1_PrevSeasons and symbolSeason3.profit_loss:
									income_statement.profit_loss = string_to_decimal(next_data.string) - symbolSeason3.profit_loss
								else:
									income_statement.profit_loss = string_to_decimal(next_data.string)
								# print('本期淨利（淨損）:' + str(income_statement.profit_loss))
						elif r'國外營運機構財務報表換算之兌換差額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.exchange_differences_on_translation = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.exchange_differences_on_translation and symbolSeason2.exchange_differences_on_translation and symbolSeason3.exchange_differences_on_translation:
									income_statement.exchange_differences_on_translation = string_to_decimal(next_data.string) - symbolSeason1.exchange_differences_on_translation - symbolSeason2.exchange_differences_on_translation - symbolSeason3.exchange_differences_on_translation
								elif has_2_PrevSeasons and symbolSeason2.exchange_differences_on_translation and symbolSeason3.exchange_differences_on_translation:
									income_statement.exchange_differences_on_translation = string_to_decimal(next_data.string) - symbolSeason2.exchange_differences_on_translation - symbolSeason3.exchange_differences_on_translation
								elif has_1_PrevSeasons and symbolSeason3.exchange_differences_on_translation:
									income_statement.exchange_differences_on_translation = string_to_decimal(next_data.string) - symbolSeason3.exchange_differences_on_translation
								else:
									income_statement.exchange_differences_on_translation = string_to_decimal(next_data.string)
								# print('國外營運機構財務報表換算之兌換差額:' + str(income_statement.exchange_differences_on_translation))
						elif r'備供出售金融資產未實現評價損益' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets and symbolSeason2.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets and symbolSeason3.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets:
									income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets - symbolSeason2.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets - symbolSeason3.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets
								elif has_2_PrevSeasons and symbolSeason2.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets and symbolSeason3.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets:
									income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets - symbolSeason3.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets
								elif has_1_PrevSeasons and symbolSeason3.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets:
									income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason3.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets
								else:
									income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								# print('備供出售金融資產未實現評價損益:' + str(income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets))		
						elif r'其他綜合損益（淨額）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.other_comprehensive_income_net = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.other_comprehensive_income_net and symbolSeason2.other_comprehensive_income_net and symbolSeason3.other_comprehensive_income_net:
									income_statement.other_comprehensive_income_net = string_to_decimal(next_data.string) - symbolSeason1.other_comprehensive_income_net - symbolSeason2.other_comprehensive_income_net - symbolSeason3.other_comprehensive_income_net
								elif has_2_PrevSeasons and symbolSeason2.other_comprehensive_income_net and symbolSeason3.other_comprehensive_income_net:
									income_statement.other_comprehensive_income_net = string_to_decimal(next_data.string) - symbolSeason2.other_comprehensive_income_net - symbolSeason3.other_comprehensive_income_net
								elif has_1_PrevSeasons and symbolSeason3.other_comprehensive_income_net:
									income_statement.other_comprehensive_income_net = string_to_decimal(next_data.string) - symbolSeason3.other_comprehensive_income_net
								else:
									income_statement.other_comprehensive_income_net = string_to_decimal(next_data.string)
								# print('其他綜合損益（淨額）:' + str(income_statement.other_comprehensive_income_net))
						elif r'本期綜合損益總額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_comprehensive_income = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_comprehensive_income and symbolSeason2.total_comprehensive_income and symbolSeason3.total_comprehensive_income:
									income_statement.total_comprehensive_income = string_to_decimal(next_data.string) - symbolSeason1.total_comprehensive_income - symbolSeason2.total_comprehensive_income - symbolSeason3.total_comprehensive_income
								elif has_2_PrevSeasons and symbolSeason2.total_comprehensive_income and symbolSeason3.total_comprehensive_income:
									income_statement.total_comprehensive_income = string_to_decimal(next_data.string) - symbolSeason2.total_comprehensive_income - symbolSeason3.total_comprehensive_income
								elif has_1_PrevSeasons and symbolSeason3.total_comprehensive_income:
									income_statement.total_comprehensive_income = string_to_decimal(next_data.string) - symbolSeason3.total_comprehensive_income
								else:
									income_statement.total_comprehensive_income = string_to_decimal(next_data.string)
								# print('本期綜合損益總額:' + str(income_statement.total_comprehensive_income))
						elif r'母公司業主（淨利／損）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.profit_loss_attributable_to_owners_of_parent = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.profit_loss_attributable_to_owners_of_parent and symbolSeason2.profit_loss_attributable_to_owners_of_parent and symbolSeason3.profit_loss_attributable_to_owners_of_parent:
									income_statement.profit_loss_attributable_to_owners_of_parent = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_attributable_to_owners_of_parent - symbolSeason2.profit_loss_attributable_to_owners_of_parent - symbolSeason3.profit_loss_attributable_to_owners_of_parent
								elif has_2_PrevSeasons and symbolSeason2.profit_loss_attributable_to_owners_of_parent and symbolSeason3.profit_loss_attributable_to_owners_of_parent:
									income_statement.profit_loss_attributable_to_owners_of_parent = string_to_decimal(next_data.string) - symbolSeason2.profit_loss_attributable_to_owners_of_parent - symbolSeason3.profit_loss_attributable_to_owners_of_parent
								elif has_1_PrevSeasons and symbolSeason3.profit_loss_attributable_to_owners_of_parent:
									income_statement.profit_loss_attributable_to_owners_of_parent = string_to_decimal(next_data.string) - symbolSeason3.profit_loss_attributable_to_owners_of_parent
								else:
									income_statement.profit_loss_attributable_to_owners_of_parent = string_to_decimal(next_data.string)
								# print('母公司業主（淨利／損）:' + str(income_statement.profit_loss_attributable_to_owners_of_parent))
						elif r'非控制權益（淨利／損）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.profit_loss_attributable_to_non_controlling_interests = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.profit_loss_attributable_to_non_controlling_interests and symbolSeason2.profit_loss_attributable_to_non_controlling_interests and symbolSeason3.profit_loss_attributable_to_non_controlling_interests:
									income_statement.profit_loss_attributable_to_non_controlling_interests = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_attributable_to_non_controlling_interests - symbolSeason2.profit_loss_attributable_to_non_controlling_interests - symbolSeason3.profit_loss_attributable_to_non_controlling_interests
								elif has_2_PrevSeasons and symbolSeason2.profit_loss_attributable_to_non_controlling_interests and symbolSeason3.profit_loss_attributable_to_non_controlling_interests:
									income_statement.profit_loss_attributable_to_non_controlling_interests = string_to_decimal(next_data.string) - symbolSeason2.profit_loss_attributable_to_non_controlling_interests - symbolSeason3.profit_loss_attributable_to_non_controlling_interests
								elif has_1_PrevSeasons and symbolSeason3.profit_loss_attributable_to_non_controlling_interests:
									income_statement.profit_loss_attributable_to_non_controlling_interests = string_to_decimal(next_data.string) - symbolSeason3.profit_loss_attributable_to_non_controlling_interests
								else:
									income_statement.profit_loss_attributable_to_non_controlling_interests = string_to_decimal(next_data.string)
								# print('非控制權益（淨利／損）:' + str(income_statement.profit_loss_attributable_to_non_controlling_interests))
						elif r'母公司業主（綜合損益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.comprehensive_income_attributable_to_owners_of_parent = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.comprehensive_income_attributable_to_owners_of_parent and symbolSeason2.comprehensive_income_attributable_to_owners_of_parent and symbolSeason3.comprehensive_income_attributable_to_owners_of_parent:
									income_statement.comprehensive_income_attributable_to_owners_of_parent = string_to_decimal(next_data.string) - symbolSeason1.comprehensive_income_attributable_to_owners_of_parent - symbolSeason2.comprehensive_income_attributable_to_owners_of_parent - symbolSeason3.comprehensive_income_attributable_to_owners_of_parent
								elif has_2_PrevSeasons and symbolSeason2.comprehensive_income_attributable_to_owners_of_parent and symbolSeason3.comprehensive_income_attributable_to_owners_of_parent:
									income_statement.comprehensive_income_attributable_to_owners_of_parent = string_to_decimal(next_data.string) - symbolSeason2.comprehensive_income_attributable_to_owners_of_parent - symbolSeason3.comprehensive_income_attributable_to_owners_of_parent
								elif has_1_PrevSeasons and symbolSeason3.comprehensive_income_attributable_to_owners_of_parent:
									income_statement.comprehensive_income_attributable_to_owners_of_parent = string_to_decimal(next_data.string) - symbolSeason3.comprehensive_income_attributable_to_owners_of_parent
								else:
									income_statement.comprehensive_income_attributable_to_owners_of_parent = string_to_decimal(next_data.string)
								# print('母公司業主（綜合損益）:' + str(income_statement.comprehensive_income_attributable_to_owners_of_parent))
						elif r'非控制權益（綜合損益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.comprehensive_income_attributable_to_non_controlling_interests = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.comprehensive_income_attributable_to_non_controlling_interests and symbolSeason2.comprehensive_income_attributable_to_non_controlling_interests and symbolSeason3.comprehensive_income_attributable_to_non_controlling_interests:
									income_statement.comprehensive_income_attributable_to_non_controlling_interests = string_to_decimal(next_data.string) - symbolSeason1.comprehensive_income_attributable_to_non_controlling_interests - symbolSeason2.comprehensive_income_attributable_to_non_controlling_interests - symbolSeason3.comprehensive_income_attributable_to_non_controlling_interests
								elif has_2_PrevSeasons and symbolSeason2.comprehensive_income_attributable_to_non_controlling_interests and symbolSeason3.comprehensive_income_attributable_to_non_controlling_interests:
									income_statement.comprehensive_income_attributable_to_non_controlling_interests = string_to_decimal(next_data.string) - symbolSeason2.comprehensive_income_attributable_to_non_controlling_interests - symbolSeason3.comprehensive_income_attributable_to_non_controlling_interests
								elif has_1_PrevSeasons and symbolSeason3.comprehensive_income_attributable_to_non_controlling_interests:
									income_statement.comprehensive_income_attributable_to_non_controlling_interests = string_to_decimal(next_data.string) - symbolSeason3.comprehensive_income_attributable_to_non_controlling_interests
								else:
									income_statement.comprehensive_income_attributable_to_non_controlling_interests = string_to_decimal(next_data.string)
								# print('非控制權益（綜合損益）:' + str(income_statement.comprehensive_income_attributable_to_non_controlling_interests))
						elif r'基本每股盈餘' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_basic_earnings_per_share = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_basic_earnings_per_share and symbolSeason2.total_basic_earnings_per_share and symbolSeason3.total_basic_earnings_per_share:
									income_statement.total_basic_earnings_per_share = string_to_decimal(next_data.string) - symbolSeason1.total_basic_earnings_per_share - symbolSeason2.total_basic_earnings_per_share - symbolSeason3.total_basic_earnings_per_share
								elif has_2_PrevSeasons and symbolSeason2.total_basic_earnings_per_share and symbolSeason3.total_basic_earnings_per_share:
									income_statement.total_basic_earnings_per_share = string_to_decimal(next_data.string) - symbolSeason2.total_basic_earnings_per_share - symbolSeason3.total_basic_earnings_per_share
								elif has_1_PrevSeasons and symbolSeason3.total_basic_earnings_per_share:
									income_statement.total_basic_earnings_per_share = string_to_decimal(next_data.string) - symbolSeason3.total_basic_earnings_per_share
								else:
									income_statement.total_basic_earnings_per_share = string_to_decimal(next_data.string)
								# print('基本每股盈餘:' + str(income_statement.total_basic_earnings_per_share))
						elif r'稀釋每股盈餘' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr != 4:
									income_statement.total_diluted_earnings_per_share = string_to_decimal(next_data.string)
								elif has_3_PrevSeasons and symbolSeason1.total_diluted_earnings_per_share and symbolSeason2.total_diluted_earnings_per_share and symbolSeason3.total_diluted_earnings_per_share:
									income_statement.total_diluted_earnings_per_share = string_to_decimal(next_data.string) - symbolSeason1.total_diluted_earnings_per_share - symbolSeason2.total_diluted_earnings_per_share - symbolSeason3.total_diluted_earnings_per_share
								elif has_2_PrevSeasons and symbolSeason2.total_diluted_earnings_per_share and symbolSeason3.total_diluted_earnings_per_share:
									income_statement.total_diluted_earnings_per_share = string_to_decimal(next_data.string) - symbolSeason2.total_diluted_earnings_per_share - symbolSeason3.total_diluted_earnings_per_share
								elif has_1_PrevSeasons and symbolSeason3.total_diluted_earnings_per_share:
									income_statement.total_diluted_earnings_per_share = string_to_decimal(next_data.string) - symbolSeason3.total_diluted_earnings_per_share
								else:
									income_statement.total_diluted_earnings_per_share = string_to_decimal(next_data.string)
								# print('稀釋每股盈餘:' + str(income_statement.total_diluted_earnings_per_share))

				response.close()
				# 確定有抓到營業收入的值，才將該檔股票資料寫入資料表中
				if income_statement.total_operating_revenue is not None:
					income_statement.save()
					print(symbol + " updated.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ") @ " + str(datetime.now()))
				else:
					print(symbol + " no data.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")

	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name":"綜合損益表(季)"})

# 綜合損益表（年）
def annual_income_statement(request):

	# 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stockfins_annualincomestatement')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	# # 輸入西元年(時間參數改由最外層控制)
	# yr = 2014

	start_time = datetime.now()
	stockID_updated = get_stockID_updated(request)

	income_statement = AnnualIncomeStatement()
	count = 0
	stocks = StockID.objects.all()[count:]
	countAll = stocks.count() # 計算全部需要更新的股票檔數

	for stock in stocks:
		symbol = stock.symbol
		mkt = stock.market
		count = count + 1
		# STEP1.跳過金融股
		if symbol[:2] == "28":
			continue
		# STEP2.檢查資料是否已經存在資料庫，如果「是」，就跳過此檔不更新，以節省時間
		id_test_exist = str(yr) + '-' + symbol
		if AnnualIncomeStatement.objects.filter(ID=id_test_exist):
			print(symbol + u"資料已存在資料庫.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ")")
			continue
		# STEP3.檢查該檔股票的財報是否已經在更新清單裡面，如果有才進行連線更新，沒有的話就跳過
		if symbol not in stockID_updated:
			print(symbol + u"網站資料尚未更新.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ")")
			continue
		# 先宣告所有報表項目
		income_statement.ID = str(yr) + '-' + symbol
		income_statement.symbol = symbol
		income_statement.year = yr
		income_statement.net_sales_revenue = None
		income_statement.total_service_revenue = None
		income_statement.total_operating_revenue = None
		income_statement.total_cost_of_sales = None
		income_statement.total_cost_of_services = None
		income_statement.total_operating_costs = None
		income_statement.gross_profit_loss_from_operations = None
		income_statement.gross_profit_loss_from_operations_net = None
		income_statement.total_selling_expenses = None
		income_statement.total_administrative_expenses = None
		income_statement.total_research_and_development_expenses = None
		income_statement.total_operating_expenses = None
		income_statement.net_operating_income_loss = None
		income_statement.total_other_income = None
		income_statement.other_gains_and_losses_net = None
		income_statement.finance_costs_net = None
		income_statement.total_non_operating_income_and_expenses = None
		income_statement.profit_loss_from_continuing_operations_before_tax = None
		income_statement.total_tax_expense_income = None
		income_statement.profit_loss_from_continuing_operations = None
		income_statement.profit_loss = None
		income_statement.exchange_differences_on_translation = None
		income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = None
		income_statement.other_comprehensive_income_net = None
		income_statement.total_comprehensive_income = None
		income_statement.profit_loss_attributable_to_owners_of_parent = None
		income_statement.profit_loss_attributable_to_non_controlling_interests = None
		income_statement.comprehensive_income_attributable_to_owners_of_parent = None
		income_statement.comprehensive_income_attributable_to_non_controlling_interests = None
		income_statement.total_basic_earnings_per_share = None
		income_statement.total_diluted_earnings_per_share = None

		# 公開資訊觀測站存放上市櫃公司綜合損益表的網址
		url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb04'
		values = {'encodeURIComponent': '1', 'step': '1', 'firstin': '1', 'off': '1',
					'keyword4': '', 'code1': '', 'TYPEK2': '', 'checkbtn': '',
					'queryName': 'co_id', 'TYPEK': 'all', 'isnew': 'false',
					'co_id': symbol, 'year': str(yr-1911), 'season': '04'}
		url_data = urllib.urlencode(values)
		headers = {'User-Agent': 'Mozilla/5.0'}
		req = urllib2.Request(url, url_data, headers)

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
			annual_income_datas = soup.find_all('td', attrs = {'style':'text-align:left;white-space:nowrap;'})
			busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
			# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
			while (busy_msg is not None):
				response.close()
				print("Server busy, Re-connect in 20 sec.")
				time.sleep(20)
				headers = {'User-Agent': 'Mozilla/4.0'}
				req = urllib2.Request(url, url_data, headers)
				try:
					response = urllib2.urlopen(req)
					print("Re-connect URL now!")
				except URLError, e:
					if hasattr(e, "reason"):
						print(symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
					elif hasattr(e, "code"):
						print(symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
				else:
					soup = BeautifulSoup(response, from_encoding = 'utf-8')
					annual_income_datas = soup.find_all('td', attrs = {'style':'text-align:left;white-space:nowrap;'})
					busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})

			# 確認一切正常之後，才將網頁內容填入資料表
			for data in annual_income_datas:
				if data.string != None:
					if r'銷貨收入淨額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.net_sales_revenue = string_to_decimal(next_data.string)
							# print('銷貨收入淨額:' + str(income_statement.net_sales_revenue))
					elif r'勞務收入' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_service_revenue = string_to_decimal(next_data.string)
							# print('勞務收入:' + str(income_statement.total_service_revenue))
					elif r'營業收入合計' in data.string.encode('utf-8') or r'收入合計' in data.string.encode('utf-8') or r'收益合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_operating_revenue = string_to_decimal(next_data.string)
							# print('營業收入合計:' + str(income_statement.total_operating_revenue))
					elif r'銷貨成本' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_cost_of_sales = string_to_decimal(next_data.string)
							# print('銷貨成本:' + str(income_statement.total_cost_of_sales))
					elif r'勞務成本' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_cost_of_services = string_to_decimal(next_data.string)
							# print('勞務成本:' + str(income_statement.total_cost_of_services))
					elif r'營業成本合計' in data.string.encode('utf-8') or r'支出合計' in data.string.encode('utf-8') or r'支出及費用合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_operating_costs = string_to_decimal(next_data.string)
							# print('營業成本合計:' + str(income_statement.total_operating_costs))
					elif r'營業毛利（毛損）' == data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.gross_profit_loss_from_operations = string_to_decimal(next_data.string)
							# print('營業毛利（毛損）:' + str(income_statement.gross_profit_loss_from_operations))
					elif r'營業毛利（毛損）淨額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.gross_profit_loss_from_operations_net = string_to_decimal(next_data.string)
							# print('營業毛利（毛損）淨額:' + str(income_statement.gross_profit_loss_from_operations_net))
					elif r'推銷費用' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_selling_expenses = string_to_decimal(next_data.string)
							# print('推銷費用:' + str(income_statement.total_selling_expenses))
					elif r'管理費用' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_administrative_expenses = string_to_decimal(next_data.string)
							# print('管理費用:' + str(income_statement.total_administrative_expenses))
					elif r'研究發展費用' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_research_and_development_expenses = string_to_decimal(next_data.string)
							# print('研究發展費用:' + str(income_statement.total_research_and_development_expenses))
					elif r'營業費用合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_operating_expenses = string_to_decimal(next_data.string)
							# print('營業費用合計:' + str(income_statement.total_operating_expenses))
					elif r'營業利益（損失）' in data.string.encode('utf-8') or r'營業利益' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.net_operating_income_loss = string_to_decimal(next_data.string)
							# print('營業利益（損失）:' + str(income_statement.net_operating_income_loss))
					elif r'其他收入' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_other_income = string_to_decimal(next_data.string)
							# print('其他收入:' + str(income_statement.total_other_income))
					elif r'其他利益及損失淨額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.other_gains_and_losses_net = string_to_decimal(next_data.string)
							# print('其他利益及損失淨額:' + str(income_statement.other_gains_and_losses_net))
					elif r'財務成本淨額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.finance_costs_net = string_to_decimal(next_data.string)
							# print('財務成本淨額:' + str(income_statement.finance_costs_net))
					elif r'營業外收入及支出合計' in data.string.encode('utf-8') or r'營業外損益合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_non_operating_income_and_expenses = string_to_decimal(next_data.string)
							# print('營業外收入及支出合計:' + str(income_statement.total_non_operating_income_and_expenses))
					elif r'稅前淨利（淨損）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string)
							# print('稅前淨利（淨損）:' + str(income_statement.profit_loss_from_continuing_operations_before_tax))
					elif r'所得稅費用（利益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_tax_expense_income = string_to_decimal(next_data.string)
							# print('所得稅費用（利益）合計:' + str(income_statement.total_tax_expense_income))
					elif r'繼續營業單位本期淨利（淨損）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.profit_loss_from_continuing_operations = string_to_decimal(next_data.string)
							# print('繼續營業單位本期淨利（淨損）:' + str(income_statement.profit_loss_from_continuing_operations))
					elif r'本期淨利（淨損）' == data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.profit_loss = string_to_decimal(next_data.string)
							# print('本期淨利（淨損）:' + str(income_statement.profit_loss))
					elif r'國外營運機構財務報表換算之兌換差額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.exchange_differences_on_translation = string_to_decimal(next_data.string)
							# print('國外營運機構財務報表換算之兌換差額:' + str(income_statement.exchange_differences_on_translation))
					elif r'備供出售金融資產未實現評價損益' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
							# print('備供出售金融資產未實現評價損益:' + str(income_statement.unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets))		
					elif r'其他綜合損益（淨額）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.other_comprehensive_income_net = string_to_decimal(next_data.string)
							# print('其他綜合損益（淨額）:' + str(income_statement.other_comprehensive_income_net))
					elif r'本期綜合損益總額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_comprehensive_income = string_to_decimal(next_data.string)
							# print('本期綜合損益總額:' + str(income_statement.total_comprehensive_income))
					elif r'母公司業主（淨利／損）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.profit_loss_attributable_to_owners_of_parent = string_to_decimal(next_data.string)
							# print('母公司業主（淨利／損）:' + str(income_statement.profit_loss_attributable_to_owners_of_parent))
					elif r'非控制權益（淨利／損）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.profit_loss_attributable_to_non_controlling_interests = string_to_decimal(next_data.string)
							# print('非控制權益（淨利／損）:' + str(income_statement.profit_loss_attributable_to_non_controlling_interests))
					elif r'母公司業主（綜合損益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.comprehensive_income_attributable_to_owners_of_parent = string_to_decimal(next_data.string)
							# print('母公司業主（綜合損益）:' + str(income_statement.comprehensive_income_attributable_to_owners_of_parent))
					elif r'非控制權益（綜合損益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.comprehensive_income_attributable_to_non_controlling_interests = string_to_decimal(next_data.string)
							# print('非控制權益（綜合損益）:' + str(income_statement.comprehensive_income_attributable_to_non_controlling_interests))
					elif r'基本每股盈餘' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_basic_earnings_per_share = string_to_decimal(next_data.string)
							# print('基本每股盈餘:' + str(income_statement.total_basic_earnings_per_share))
					elif r'稀釋每股盈餘' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							income_statement.total_diluted_earnings_per_share = string_to_decimal(next_data.string)
							# print('稀釋每股盈餘:' + str(income_statement.total_diluted_earnings_per_share))

			response.close()
			# 確定有抓到EPS的值，才將該檔股票資料寫入資料表中
			if income_statement.total_operating_revenue is not None:
				income_statement.save()
				print(symbol + " updated.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ") @ " + str(datetime.now()))
			else:
				print(symbol + " no data.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ")")

	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name":"綜合損益表(年)"})

# 現金流量表（季）
def season_cash_flow(request):

	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stockfins_seasoncashflow')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	# # 輸入西元年(時間參數改由最外層控制)
	# yr = 2014 
	# season = [2]

	start_time = datetime.now()
	stockID_updated = get_stockID_updated(request)

	for qtr in season:
		cash_flow = SeasonCashFlow()
		count = 0
		stocks = StockID.objects.all()[count:]
		countAll = stocks.count() # 計算全部需要更新的股票檔數

		if qtr != 1:
			# 若不是Q1，則先將可能存在的Q3,Q2,Q1物件取出
			cashFlowSeason1 = SeasonCashFlow.objects.filter(year=yr, season="Q1")
			cashFlowSeason2 = SeasonCashFlow.objects.filter(year=yr, season="Q2")
			cashFlowSeason3 = SeasonCashFlow.objects.filter(year=yr, season="Q3")

		for stock in stocks:
			symbol = stock.symbol
			mkt = stock.market
			count = count + 1
			# STEP1.跳過金融股
			if symbol[:2] == "28":
				continue
			# STEP2.檢查資料是否已經存在資料庫，如果「是」，就跳過此檔不更新，以節省時間
			id_test_exist = str(yr) + 'Q' + str(qtr) + '-' + symbol
			if SeasonCashFlow.objects.filter(ID=id_test_exist):
				print(symbol + u"資料已存在資料庫.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")
				continue
			# STEP3.檢查該檔股票的財報是否已經在更新清單裡面，如果有才進行連線更新，沒有的話就跳過
			if symbol not in stockID_updated:
				print(symbol + u"網站資料尚未更新.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")
				continue
			# 先宣告所有報表項目
			cash_flow.ID = str(yr) + 'Q' + str(qtr) + '-' + symbol
			cash_flow.symbol = symbol
			cash_flow.year = yr
			cash_flow.season = 'Q' + str(qtr)
			cash_flow.date = str(yr) + 'Q' + str(qtr)
			cash_flow.profit_loss_from_continuing_operations_before_tax = None
			cash_flow.profit_loss_before_tax = None
			cash_flow.depreciation_expense = None
			cash_flow.amortization_expense = None
			cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = None
			cash_flow.interest_expense = None
			cash_flow.interest_income = None
			cash_flow.share_based_payments = None
			cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = None
			cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = None
			cash_flow.loss_gain_on_disposal_of_investments = None
			cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = None
			cash_flow.realized_loss_profit_on_from_sales = None
			cash_flow.unrealized_foreign_exchange_loss_gain = None
			cash_flow.other_adjustments_to_reconcile_profit_loss = None
			cash_flow.total_adjustments_to_reconcile_profit_loss = None
			cash_flow.decrease_increase_in_financial_assets_held_for_trading = None
			cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = None
			cash_flow.decrease_increase_in_notes_receivable = None
			cash_flow.decrease_increase_in_accounts_receivable = None
			cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = None
			cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = None
			cash_flow.decrease_increase_in_inventories = None
			cash_flow.decrease_increase_in_prepayments = None
			cash_flow.decrease_increase_in_other_current_assets = None
			cash_flow.decrease_increase_in_other_financial_assets = None
			cash_flow.decrease_increase_in_other_operating_assets = None
			cash_flow.total_changes_in_operating_assets = None
			cash_flow.increase_decrease_in_accounts_payable = None
			cash_flow.increase_decrease_in_accounts_payable_to_related_parties = None
			cash_flow.increase_decrease_in_other_payable = None
			cash_flow.increase_decrease_in_provisions = None
			cash_flow.increase_decrease_in_other_current_liabilities = None
			cash_flow.increase_decrease_in_accrued_pension_liabilities = None
			cash_flow.total_changes_in_operating_liabilities = None
			cash_flow.total_changes_in_operating_assets_and_liabilities = None
			cash_flow.total_adjustments = None
			cash_flow.cash_inflow_outflow_generated_from_operations = None
			cash_flow.income_taxes_refund_paid = None
			cash_flow.net_cash_flows_from_used_in_operating_activities = None
			cash_flow.acquisition_of_available_for_sale_financial_assets = None
			cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = None
			cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = None
			cash_flow.acquisition_of_financial_assets_at_cost = None
			cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = None
			cash_flow.acquisition_of_property_plant_and_equipment = None
			cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = None
			cash_flow.acquisition_of_intangible_assets = None
			cash_flow.increase_in_other_non_current_assets = None
			cash_flow.net_cash_flows_from_used_in_investing_activities = None
			cash_flow.increase_in_short_term_loans = None
			cash_flow.decrease_in_short_term_loans = None
			cash_flow.increase_in_short_term_notes_and_bills_payable = None
			cash_flow.decrease_in_short_term_notes_and_bills_payable = None
			cash_flow.proceeds_from_issuing_bonds = None
			cash_flow.repayments_of_bonds = None
			cash_flow.proceeds_from_long_term_debt = None
			cash_flow.repayments_of_long_term_debt = None
			cash_flow.payments_to_acquire_treasury_shares = None
			cash_flow.proceeds_from_sale_of_treasury_shares = None
			cash_flow.cash_dividends_paid
			cash_flow.net_cash_flows_from_used_in_financing_activities = None
			cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = None
			cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = None
			cash_flow.cash_and_cash_equivalents_at_beginning_of_period = None
			cash_flow.cash_and_cash_equivalents_at_end_of_period = None
			cash_flow.cash_and_cash_equivalents_reported_in_the_statement_of_financial_position = None
			cash_flow.free_cash_flow = None

			symbolSeason1 = None
			symbolSeason2 = None
			symbolSeason3 = None
			has_3_PrevSeasons = False
			has_2_PrevSeasons = False
			has_1_PrevSeasons = False

			# 抓Q4資料之前，先將該檔股票Q3,Q2,Q1的資料取出(不一定都有)，並依存在情況定義has_n_PreSeasons為True
			if qtr == 4:
				if cashFlowSeason1:
					if cashFlowSeason1.filter(symbol=symbol):
						symbolSeason1 = cashFlowSeason1.get(symbol=symbol)
				if cashFlowSeason2:
					if cashFlowSeason2.filter(symbol=symbol):
						symbolSeason2 = cashFlowSeason2.get(symbol=symbol)
				if cashFlowSeason3:
					if cashFlowSeason3.filter(symbol=symbol):
						symbolSeason3 = cashFlowSeason3.get(symbol=symbol)
				if symbolSeason1 and symbolSeason2 and symbolSeason3:
					has_3_PrevSeasons = True
				elif symbolSeason2 and symbolSeason3:
					has_2_PrevSeasons = True
				elif symbolSeason3:
					has_1_PrevSeasons = True
			elif qtr == 3:
				if cashFlowSeason1:
					if cashFlowSeason1.filter(symbol=symbol):
						symbolSeason1 = cashFlowSeason1.get(symbol=symbol)
				if cashFlowSeason2:
					if cashFlowSeason2.filter(symbol=symbol):
						symbolSeason2 = cashFlowSeason2.get(symbol=symbol)
				if symbolSeason1 and symbolSeason2:
					has_2_PrevSeasons = True
				elif symbolSeason2:
					has_1_PrevSeasons = True
			elif qtr == 2:
				if cashFlowSeason1:
					if cashFlowSeason1.filter(symbol=symbol):
						symbolSeason1 = cashFlowSeason1.get(symbol=symbol)
				if symbolSeason1:
					has_1_PrevSeasons = True

			# 公開資訊觀測站存放上市櫃公司綜合損益表的網址
			url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb05'
			values = {'encodeURIComponent': '1', 'step': '1', 'firstin': '1', 'off': '1',
						'keyword4': '', 'code1': '', 'TYPEK2': '', 'checkbtn': '',
						'queryName': 'co_id', 'TYPEK': 'all', 'isnew': 'false',
						'co_id': symbol, 'year': str(yr-1911), 'season': str(qtr).zfill(2)}
			url_data = urllib.urlencode(values)
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib2.Request(url, url_data, headers)

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
				season_cashflow_datas = soup.find_all('td',
												attrs = {'style':'text-align:left;white-space:nowrap;'})
				busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
				
				# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
				while (busy_msg is not None):
					response.close()
					print("Server busy, Re-connect in 20 sec.")
					time.sleep(20)
					headers = {'User-Agent': 'Mozilla/4.0'}
					req = urllib2.Request(url, url_data, headers)
					try:
						response = urllib2.urlopen(req)
						print("Re-connect URL now!")
					except URLError, e:
						if hasattr(e, "reason"):
							print(symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
						elif hasattr(e, "code"):
							print(symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
					else:
						soup = BeautifulSoup(response, from_encoding = 'utf-8')
						season_cashflow_datas = soup.find_all('td',
												attrs = {'style':'text-align:left;white-space:nowrap;'})
						busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})	
				
				# 確認一切正常之後，才將網頁內容填入資料表
				for data in season_cashflow_datas:
					if data.string != None:
						if r'繼續營業單位稅前淨利（淨損）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.profit_loss_from_continuing_operations_before_tax and symbolSeason2.profit_loss_from_continuing_operations_before_tax and symbolSeason3.profit_loss_from_continuing_operations_before_tax:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_from_continuing_operations_before_tax - symbolSeason2.profit_loss_from_continuing_operations_before_tax - symbolSeason3.profit_loss_from_continuing_operations_before_tax
									elif has_2_PrevSeasons and symbolSeason2.profit_loss_from_continuing_operations_before_tax and symbolSeason3.profit_loss_from_continuing_operations_before_tax:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason2.profit_loss_from_continuing_operations_before_tax - symbolSeason3.profit_loss_from_continuing_operations_before_tax
									elif has_1_PrevSeasons and symbolSeason3.profit_loss_from_continuing_operations_before_tax:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason3.profit_loss_from_continuing_operations_before_tax
									else:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.profit_loss_from_continuing_operations_before_tax and symbolSeason2.profit_loss_from_continuing_operations_before_tax:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_from_continuing_operations_before_tax - symbolSeason2.profit_loss_from_continuing_operations_before_tax
									elif has_1_PrevSeasons and symbolSeason2.profit_loss_from_continuing_operations_before_tax:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason2.profit_loss_from_continuing_operations_before_tax
									else:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.profit_loss_from_continuing_operations_before_tax:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_from_continuing_operations_before_tax
									else:
										cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string)
								# print('繼續營業單位稅前淨利（淨損）:' + str(cash_flow.profit_loss_from_continuing_operations_before_tax))
						elif r'本期稅前淨利（淨損）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.profit_loss_before_tax and symbolSeason2.profit_loss_before_tax and symbolSeason3.profit_loss_before_tax:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_before_tax - symbolSeason2.profit_loss_before_tax - symbolSeason3.profit_loss_before_tax
									elif has_2_PrevSeasons and symbolSeason2.profit_loss_before_tax and symbolSeason3.profit_loss_before_tax:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string) - symbolSeason2.profit_loss_before_tax - symbolSeason3.profit_loss_before_tax
									elif has_1_PrevSeasons and symbolSeason3.profit_loss_before_tax:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string) - symbolSeason3.profit_loss_before_tax
									else:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.profit_loss_before_tax and symbolSeason2.profit_loss_before_tax:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_before_tax - symbolSeason2.profit_loss_before_tax
									elif has_1_PrevSeasons and symbolSeason2.profit_loss_before_tax:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string) - symbolSeason2.profit_loss_before_tax
									else:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.profit_loss_before_tax:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string) - symbolSeason1.profit_loss_before_tax
									else:
										cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string)
								# print('本期稅前淨利（淨損）:' + str(cash_flow.profit_loss_before_tax))
						elif r'折舊費用' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.depreciation_expense = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.depreciation_expense and symbolSeason2.depreciation_expense and symbolSeason3.depreciation_expense:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string) - symbolSeason1.depreciation_expense - symbolSeason2.depreciation_expense - symbolSeason3.depreciation_expense
									elif has_2_PrevSeasons and symbolSeason2.depreciation_expense and symbolSeason3.depreciation_expense:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string) - symbolSeason2.depreciation_expense - symbolSeason3.depreciation_expense
									elif has_1_PrevSeasons and symbolSeason3.depreciation_expense:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string) - symbolSeason3.depreciation_expense
									else:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.depreciation_expense and symbolSeason2.depreciation_expense:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string) - symbolSeason1.depreciation_expense - symbolSeason2.depreciation_expense
									elif has_1_PrevSeasons and symbolSeason2.depreciation_expense:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string) - symbolSeason2.depreciation_expense
									else:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.depreciation_expense:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string) - symbolSeason1.depreciation_expense
									else:
										cash_flow.depreciation_expense = string_to_decimal(next_data.string)
								# print('折舊費用:' + str(cash_flow.depreciation_expense))
						elif r'攤銷費用' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.amortization_expense = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.amortization_expense and symbolSeason2.amortization_expense and symbolSeason3.amortization_expense:
										cash_flow.amortization_expense = string_to_decimal(next_data.string) - symbolSeason1.amortization_expense - symbolSeason2.amortization_expense - symbolSeason3.amortization_expense
									elif has_2_PrevSeasons and symbolSeason2.amortization_expense and symbolSeason3.amortization_expense:
										cash_flow.amortization_expense = string_to_decimal(next_data.string) - symbolSeason2.amortization_expense - symbolSeason3.amortization_expense
									elif has_1_PrevSeasons and symbolSeason3.amortization_expense:
										cash_flow.amortization_expense = string_to_decimal(next_data.string) - symbolSeason3.amortization_expense
									else:
										cash_flow.amortization_expense = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.amortization_expense and symbolSeason2.amortization_expense:
										cash_flow.amortization_expense = string_to_decimal(next_data.string) - symbolSeason1.amortization_expense - symbolSeason2.amortization_expense
									elif has_1_PrevSeasons and symbolSeason2.amortization_expense:
										cash_flow.amortization_expense = string_to_decimal(next_data.string) - symbolSeason2.amortization_expense
									else:
										cash_flow.amortization_expense = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.amortization_expense:
										cash_flow.amortization_expense = string_to_decimal(next_data.string) - symbolSeason1.amortization_expense
									else:
										cash_flow.amortization_expense = string_to_decimal(next_data.string)
								# print('攤銷費用:' + str(cash_flow.amortization_expense))
						elif r'透過損益按公允價值衡量金融資產及負債之淨損失（利益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss and symbolSeason2.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss and symbolSeason3.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string) - symbolSeason1.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss - symbolSeason2.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss - symbolSeason3.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss
									elif has_2_PrevSeasons and symbolSeason2.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss and symbolSeason3.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string) - symbolSeason2.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss - symbolSeason3.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss
									elif has_1_PrevSeasons and symbolSeason3.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string) - symbolSeason3.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss
									else:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss and symbolSeason2.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string) - symbolSeason1.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss - symbolSeason2.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss
									elif has_1_PrevSeasons and symbolSeason2.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string) - symbolSeason2.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss
									else:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string) - symbolSeason1.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss
									else:
										cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string)
								# print('透過損益按公允價值衡量金融資產及負債之淨損失（利益）:' + str(cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss))
						elif r'利息費用' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.interest_expense = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.interest_expense and symbolSeason2.interest_expense and symbolSeason3.interest_expense:
										cash_flow.interest_expense = string_to_decimal(next_data.string) - symbolSeason1.interest_expense - symbolSeason2.interest_expense - symbolSeason3.interest_expense
									elif has_2_PrevSeasons and symbolSeason2.interest_expense and symbolSeason3.interest_expense:
										cash_flow.interest_expense = string_to_decimal(next_data.string) - symbolSeason2.interest_expense - symbolSeason3.interest_expense
									elif has_1_PrevSeasons and symbolSeason3.interest_expense:
										cash_flow.interest_expense = string_to_decimal(next_data.string) - symbolSeason3.interest_expense
									else:
										cash_flow.interest_expense = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.interest_expense and symbolSeason2.interest_expense:
										cash_flow.interest_expense = string_to_decimal(next_data.string) - symbolSeason1.interest_expense - symbolSeason2.interest_expense
									elif has_1_PrevSeasons and symbolSeason2.interest_expense:
										cash_flow.interest_expense = string_to_decimal(next_data.string) - symbolSeason2.interest_expense
									else:
										cash_flow.interest_expense = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.interest_expense:
										cash_flow.interest_expense = string_to_decimal(next_data.string) - symbolSeason1.interest_expense
									else:
										cash_flow.interest_expense = string_to_decimal(next_data.string)
								# print('利息費用:' + str(cash_flow.interest_expense))
						elif r'利息收入' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.interest_income = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.interest_income and symbolSeason2.interest_income and symbolSeason3.interest_income:
										cash_flow.interest_income = string_to_decimal(next_data.string) - symbolSeason1.interest_income - symbolSeason2.interest_income - symbolSeason3.interest_income
									elif has_2_PrevSeasons and symbolSeason2.interest_income and symbolSeason3.interest_income:
										cash_flow.interest_income = string_to_decimal(next_data.string) - symbolSeason2.interest_income - symbolSeason3.interest_income
									elif has_1_PrevSeasons and symbolSeason3.interest_income:
										cash_flow.interest_income = string_to_decimal(next_data.string) - symbolSeason3.interest_income
									else:
										cash_flow.interest_income = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.interest_income and symbolSeason2.interest_income:
										cash_flow.interest_income = string_to_decimal(next_data.string) - symbolSeason1.interest_income - symbolSeason2.interest_income
									elif has_1_PrevSeasons and symbolSeason2.interest_income:
										cash_flow.interest_income = string_to_decimal(next_data.string) - symbolSeason2.interest_income
									else:
										cash_flow.interest_income = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.interest_income:
										cash_flow.interest_income = string_to_decimal(next_data.string) - symbolSeason1.interest_income
									else:
										cash_flow.interest_income = string_to_decimal(next_data.string)
								# print('利息收入:' + str(cash_flow.interest_income))
						elif r'股份基礎給付酬勞成本' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.share_based_payments = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.share_based_payments and symbolSeason2.share_based_payments and symbolSeason3.share_based_payments:
										cash_flow.share_based_payments = string_to_decimal(next_data.string) - symbolSeason1.share_based_payments - symbolSeason2.share_based_payments - symbolSeason3.share_based_payments
									elif has_2_PrevSeasons and symbolSeason2.share_based_payments and symbolSeason3.share_based_payments:
										cash_flow.share_based_payments = string_to_decimal(next_data.string) - symbolSeason2.share_based_payments - symbolSeason3.share_based_payments
									elif has_1_PrevSeasons and symbolSeason3.share_based_payments:
										cash_flow.share_based_payments = string_to_decimal(next_data.string) - symbolSeason3.share_based_payments
									else:
										cash_flow.share_based_payments = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.share_based_payments and symbolSeason2.share_based_payments:
										cash_flow.share_based_payments = string_to_decimal(next_data.string) - symbolSeason1.share_based_payments - symbolSeason2.share_based_payments
									elif has_1_PrevSeasons and symbolSeason2.share_based_payments:
										cash_flow.share_based_payments = string_to_decimal(next_data.string) - symbolSeason2.share_based_payments
									else:
										cash_flow.share_based_payments = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.share_based_payments:
										cash_flow.share_based_payments = string_to_decimal(next_data.string) - symbolSeason1.share_based_payments
									else:
										cash_flow.share_based_payments = string_to_decimal(next_data.string)
								# print('股份基礎給付酬勞成本:' + str(cash_flow.share_based_payments))
						elif r'採用權益法認列之關聯企業及合資損失（利益）之份額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method and symbolSeason2.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method and symbolSeason3.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason1.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method - symbolSeason2.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method - symbolSeason3.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method
									elif has_2_PrevSeasons and symbolSeason2.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method and symbolSeason3.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason2.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method - symbolSeason3.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method
									elif has_1_PrevSeasons and symbolSeason3.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason3.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method
									else:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method and symbolSeason2.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason1.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method - symbolSeason2.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method
									elif has_1_PrevSeasons and symbolSeason2.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason2.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method
									else:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason1.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method
									else:
										cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								# print('採用權益法認列之關聯企業及合資損失（利益）之份額:' + str(cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method))
						elif r'處分及報廢不動產、廠房及設備損失（利益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_property_plan_and_equipment and symbolSeason2.loss_gain_on_disposal_of_property_plan_and_equipment and symbolSeason3.loss_gain_on_disposal_of_property_plan_and_equipment:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_property_plan_and_equipment - symbolSeason2.loss_gain_on_disposal_of_property_plan_and_equipment - symbolSeason3.loss_gain_on_disposal_of_property_plan_and_equipment
									elif has_2_PrevSeasons and symbolSeason2.loss_gain_on_disposal_of_property_plan_and_equipment and symbolSeason3.loss_gain_on_disposal_of_property_plan_and_equipment:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string) - symbolSeason2.loss_gain_on_disposal_of_property_plan_and_equipment - symbolSeason3.loss_gain_on_disposal_of_property_plan_and_equipment
									elif has_1_PrevSeasons and symbolSeason3.loss_gain_on_disposal_of_property_plan_and_equipment:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string) - symbolSeason3.loss_gain_on_disposal_of_property_plan_and_equipment
									else:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_property_plan_and_equipment and symbolSeason2.loss_gain_on_disposal_of_property_plan_and_equipment:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_property_plan_and_equipment - symbolSeason2.loss_gain_on_disposal_of_property_plan_and_equipment
									elif has_1_PrevSeasons and symbolSeason2.loss_gain_on_disposal_of_property_plan_and_equipment:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string) - symbolSeason2.loss_gain_on_disposal_of_property_plan_and_equipment
									else:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_property_plan_and_equipment:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_property_plan_and_equipment
									else:
										cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string)
								# print('處分及報廢不動產、廠房及設備損失（利益）:' + str(cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment))
						elif r'處分投資損失（利益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_investments and symbolSeason2.loss_gain_on_disposal_of_investments and symbolSeason3.loss_gain_on_disposal_of_investments:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_investments - symbolSeason2.loss_gain_on_disposal_of_investments - symbolSeason3.loss_gain_on_disposal_of_investments
									elif has_2_PrevSeasons and symbolSeason2.loss_gain_on_disposal_of_investments and symbolSeason3.loss_gain_on_disposal_of_investments:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string) - symbolSeason2.loss_gain_on_disposal_of_investments - symbolSeason3.loss_gain_on_disposal_of_investments
									elif has_1_PrevSeasons and symbolSeason3.loss_gain_on_disposal_of_investments:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string) - symbolSeason3.loss_gain_on_disposal_of_investments
									else:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_investments and symbolSeason2.loss_gain_on_disposal_of_investments:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_investments - symbolSeason2.loss_gain_on_disposal_of_investments
									elif has_1_PrevSeasons and symbolSeason2.loss_gain_on_disposal_of_investments:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string) - symbolSeason2.loss_gain_on_disposal_of_investments
									else:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_investments:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_investments
									else:
										cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string)
								# print('處分投資損失（利益）:' + str(cash_flow.loss_gain_on_disposal_of_investments))
						elif r'處分採用權益法之投資損失（利益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method and symbolSeason2.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method and symbolSeason3.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method - symbolSeason2.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method - symbolSeason3.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method
									elif has_2_PrevSeasons and symbolSeason2.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method and symbolSeason3.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason2.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method - symbolSeason3.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method
									elif has_1_PrevSeasons and symbolSeason3.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason3.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method
									else:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method and symbolSeason2.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method - symbolSeason2.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method
									elif has_1_PrevSeasons and symbolSeason2.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason2.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method
									else:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string) - symbolSeason1.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method
									else:
										cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string)
								# print('處分採用權益法之投資損失（利益）:' + str(cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method))
						elif r'已實現銷貨損失（利益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.realized_loss_profit_on_from_sales and symbolSeason2.realized_loss_profit_on_from_sales and symbolSeason3.realized_loss_profit_on_from_sales:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string) - symbolSeason1.realized_loss_profit_on_from_sales - symbolSeason2.realized_loss_profit_on_from_sales - symbolSeason3.realized_loss_profit_on_from_sales
									elif has_2_PrevSeasons and symbolSeason2.realized_loss_profit_on_from_sales and symbolSeason3.realized_loss_profit_on_from_sales:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string) - symbolSeason2.realized_loss_profit_on_from_sales - symbolSeason3.realized_loss_profit_on_from_sales
									elif has_1_PrevSeasons and symbolSeason3.realized_loss_profit_on_from_sales:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string) - symbolSeason3.realized_loss_profit_on_from_sales
									else:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.realized_loss_profit_on_from_sales and symbolSeason2.realized_loss_profit_on_from_sales:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string) - symbolSeason1.realized_loss_profit_on_from_sales - symbolSeason2.realized_loss_profit_on_from_sales
									elif has_1_PrevSeasons and symbolSeason2.realized_loss_profit_on_from_sales:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string) - symbolSeason2.realized_loss_profit_on_from_sales
									else:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.realized_loss_profit_on_from_sales:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string) - symbolSeason1.realized_loss_profit_on_from_sales
									else:
										cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string)
								# print('已實現銷貨損失（利益）:' + str(cash_flow.realized_loss_profit_on_from_sales))
						elif r'未實現外幣兌換損失（利益）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.unrealized_foreign_exchange_loss_gain and symbolSeason2.unrealized_foreign_exchange_loss_gain and symbolSeason3.unrealized_foreign_exchange_loss_gain:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string) - symbolSeason1.unrealized_foreign_exchange_loss_gain - symbolSeason2.unrealized_foreign_exchange_loss_gain - symbolSeason3.unrealized_foreign_exchange_loss_gain
									elif has_2_PrevSeasons and symbolSeason2.unrealized_foreign_exchange_loss_gain and symbolSeason3.unrealized_foreign_exchange_loss_gain:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string) - symbolSeason2.unrealized_foreign_exchange_loss_gain - symbolSeason3.unrealized_foreign_exchange_loss_gain
									elif has_1_PrevSeasons and symbolSeason3.unrealized_foreign_exchange_loss_gain:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string) - symbolSeason3.unrealized_foreign_exchange_loss_gain
									else:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.unrealized_foreign_exchange_loss_gain and symbolSeason2.unrealized_foreign_exchange_loss_gain:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string) - symbolSeason1.unrealized_foreign_exchange_loss_gain - symbolSeason2.unrealized_foreign_exchange_loss_gain
									elif has_1_PrevSeasons and symbolSeason2.unrealized_foreign_exchange_loss_gain:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string) - symbolSeason2.unrealized_foreign_exchange_loss_gain
									else:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.unrealized_foreign_exchange_loss_gain:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string) - symbolSeason1.unrealized_foreign_exchange_loss_gain
									else:
										cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string)
								# print('未實現外幣兌換損失（利益）:' + str(cash_flow.unrealized_foreign_exchange_loss_gain))
						elif r'其他項目' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.other_adjustments_to_reconcile_profit_loss and symbolSeason2.other_adjustments_to_reconcile_profit_loss and symbolSeason3.other_adjustments_to_reconcile_profit_loss:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason1.other_adjustments_to_reconcile_profit_loss - symbolSeason2.other_adjustments_to_reconcile_profit_loss - symbolSeason3.other_adjustments_to_reconcile_profit_loss
									elif has_2_PrevSeasons and symbolSeason2.other_adjustments_to_reconcile_profit_loss and symbolSeason3.other_adjustments_to_reconcile_profit_loss:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason2.other_adjustments_to_reconcile_profit_loss - symbolSeason3.other_adjustments_to_reconcile_profit_loss
									elif has_1_PrevSeasons and symbolSeason3.other_adjustments_to_reconcile_profit_loss:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason3.other_adjustments_to_reconcile_profit_loss
									else:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.other_adjustments_to_reconcile_profit_loss and symbolSeason2.other_adjustments_to_reconcile_profit_loss:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason1.other_adjustments_to_reconcile_profit_loss - symbolSeason2.other_adjustments_to_reconcile_profit_loss
									elif has_1_PrevSeasons and symbolSeason2.other_adjustments_to_reconcile_profit_loss:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason2.other_adjustments_to_reconcile_profit_loss
									else:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.other_adjustments_to_reconcile_profit_loss:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason1.other_adjustments_to_reconcile_profit_loss
									else:
										cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
								# print('其他項目:' + str(cash_flow.other_adjustments_to_reconcile_profit_loss))
						elif r'不影響現金流量之收益費損項目合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.total_adjustments_to_reconcile_profit_loss and symbolSeason2.total_adjustments_to_reconcile_profit_loss and symbolSeason3.total_adjustments_to_reconcile_profit_loss:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason1.total_adjustments_to_reconcile_profit_loss - symbolSeason2.total_adjustments_to_reconcile_profit_loss - symbolSeason3.total_adjustments_to_reconcile_profit_loss
									elif has_2_PrevSeasons and symbolSeason2.total_adjustments_to_reconcile_profit_loss and symbolSeason3.total_adjustments_to_reconcile_profit_loss:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason2.total_adjustments_to_reconcile_profit_loss - symbolSeason3.total_adjustments_to_reconcile_profit_loss
									elif has_1_PrevSeasons and symbolSeason3.total_adjustments_to_reconcile_profit_loss:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason3.total_adjustments_to_reconcile_profit_loss
									else:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.total_adjustments_to_reconcile_profit_loss and symbolSeason2.total_adjustments_to_reconcile_profit_loss:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason1.total_adjustments_to_reconcile_profit_loss - symbolSeason2.total_adjustments_to_reconcile_profit_loss
									elif has_1_PrevSeasons and symbolSeason2.total_adjustments_to_reconcile_profit_loss:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason2.total_adjustments_to_reconcile_profit_loss
									else:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.total_adjustments_to_reconcile_profit_loss:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string) - symbolSeason1.total_adjustments_to_reconcile_profit_loss
									else:
										cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
								# print('不影響現金流量之收益費損項目合計:' + str(cash_flow.total_adjustments_to_reconcile_profit_loss))
						elif r'持有供交易之金融資產（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_financial_assets_held_for_trading and symbolSeason2.decrease_increase_in_financial_assets_held_for_trading and symbolSeason3.decrease_increase_in_financial_assets_held_for_trading:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_financial_assets_held_for_trading - symbolSeason2.decrease_increase_in_financial_assets_held_for_trading - symbolSeason3.decrease_increase_in_financial_assets_held_for_trading
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_financial_assets_held_for_trading and symbolSeason3.decrease_increase_in_financial_assets_held_for_trading:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_financial_assets_held_for_trading - symbolSeason3.decrease_increase_in_financial_assets_held_for_trading
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_financial_assets_held_for_trading:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_financial_assets_held_for_trading
									else:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_financial_assets_held_for_trading and symbolSeason2.decrease_increase_in_financial_assets_held_for_trading:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_financial_assets_held_for_trading - symbolSeason2.decrease_increase_in_financial_assets_held_for_trading
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_financial_assets_held_for_trading:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_financial_assets_held_for_trading
									else:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_financial_assets_held_for_trading:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_financial_assets_held_for_trading
									else:
										cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string)
								# print('持有供交易之金融資產（增加）減少:' + str(cash_flow.decrease_increase_in_financial_assets_held_for_trading))
						elif r'避險之衍生金融資產（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_derivative_financial_assets_for_hedging and symbolSeason2.decrease_increase_in_derivative_financial_assets_for_hedging and symbolSeason3.decrease_increase_in_derivative_financial_assets_for_hedging:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_derivative_financial_assets_for_hedging - symbolSeason2.decrease_increase_in_derivative_financial_assets_for_hedging - symbolSeason3.decrease_increase_in_derivative_financial_assets_for_hedging
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_derivative_financial_assets_for_hedging and symbolSeason3.decrease_increase_in_derivative_financial_assets_for_hedging:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_derivative_financial_assets_for_hedging - symbolSeason3.decrease_increase_in_derivative_financial_assets_for_hedging
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_derivative_financial_assets_for_hedging:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_derivative_financial_assets_for_hedging
									else:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_derivative_financial_assets_for_hedging and symbolSeason2.decrease_increase_in_derivative_financial_assets_for_hedging:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_derivative_financial_assets_for_hedging - symbolSeason2.decrease_increase_in_derivative_financial_assets_for_hedging
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_derivative_financial_assets_for_hedging:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_derivative_financial_assets_for_hedging
									else:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_derivative_financial_assets_for_hedging:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_derivative_financial_assets_for_hedging
									else:
										cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string)
								# print('避險之衍生金融資產（增加）減少:' + str(cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging))
						elif r'應收票據（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_notes_receivable and symbolSeason2.decrease_increase_in_notes_receivable and symbolSeason3.decrease_increase_in_notes_receivable:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_notes_receivable - symbolSeason2.decrease_increase_in_notes_receivable - symbolSeason3.decrease_increase_in_notes_receivable
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_notes_receivable and symbolSeason3.decrease_increase_in_notes_receivable:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_notes_receivable - symbolSeason3.decrease_increase_in_notes_receivable
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_notes_receivable:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_notes_receivable
									else:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_notes_receivable and symbolSeason2.decrease_increase_in_notes_receivable:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_notes_receivable - symbolSeason2.decrease_increase_in_notes_receivable
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_notes_receivable:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_notes_receivable
									else:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_notes_receivable:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_notes_receivable
									else:
										cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string)
								# print('應收票據（增加）減少:' + str(cash_flow.decrease_increase_in_notes_receivable))
						elif r'應收帳款（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_accounts_receivable and symbolSeason2.decrease_increase_in_accounts_receivable and symbolSeason3.decrease_increase_in_accounts_receivable:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_accounts_receivable - symbolSeason2.decrease_increase_in_accounts_receivable - symbolSeason3.decrease_increase_in_accounts_receivable
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_accounts_receivable and symbolSeason3.decrease_increase_in_accounts_receivable:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_accounts_receivable - symbolSeason3.decrease_increase_in_accounts_receivable
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_accounts_receivable:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_accounts_receivable
									else:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_accounts_receivable and symbolSeason2.decrease_increase_in_accounts_receivable:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_accounts_receivable - symbolSeason2.decrease_increase_in_accounts_receivable
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_accounts_receivable:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_accounts_receivable
									else:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_accounts_receivable:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_accounts_receivable
									else:
										cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string)
								# print('應收帳款（增加）減少:' + str(cash_flow.decrease_increase_in_accounts_receivable))
						elif r'應收帳款－關係人（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_accounts_receivable_due_from_related_parties and symbolSeason2.decrease_increase_in_accounts_receivable_due_from_related_parties and symbolSeason3.decrease_increase_in_accounts_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_accounts_receivable_due_from_related_parties - symbolSeason2.decrease_increase_in_accounts_receivable_due_from_related_parties - symbolSeason3.decrease_increase_in_accounts_receivable_due_from_related_parties
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_accounts_receivable_due_from_related_parties and symbolSeason3.decrease_increase_in_accounts_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_accounts_receivable_due_from_related_parties - symbolSeason3.decrease_increase_in_accounts_receivable_due_from_related_parties
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_accounts_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_accounts_receivable_due_from_related_parties
									else:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_accounts_receivable_due_from_related_parties and symbolSeason2.decrease_increase_in_accounts_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_accounts_receivable_due_from_related_parties - symbolSeason2.decrease_increase_in_accounts_receivable_due_from_related_parties
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_accounts_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_accounts_receivable_due_from_related_parties
									else:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_accounts_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_accounts_receivable_due_from_related_parties
									else:
										cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string)
								# print('應收帳款－關係人（增加）減少:' + str(cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties))
						elif r'其他應收款－關係人（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_other_receivable_due_from_related_parties and symbolSeason2.decrease_increase_in_other_receivable_due_from_related_parties and symbolSeason3.decrease_increase_in_other_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_receivable_due_from_related_parties - symbolSeason2.decrease_increase_in_other_receivable_due_from_related_parties - symbolSeason3.decrease_increase_in_other_receivable_due_from_related_parties
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_other_receivable_due_from_related_parties and symbolSeason3.decrease_increase_in_other_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_other_receivable_due_from_related_parties - symbolSeason3.decrease_increase_in_other_receivable_due_from_related_parties
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_other_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_other_receivable_due_from_related_parties
									else:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_other_receivable_due_from_related_parties and symbolSeason2.decrease_increase_in_other_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_receivable_due_from_related_parties - symbolSeason2.decrease_increase_in_other_receivable_due_from_related_parties
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_other_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_other_receivable_due_from_related_parties
									else:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_other_receivable_due_from_related_parties:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_receivable_due_from_related_parties
									else:
										cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string)
								# print('其他應收款－關係人（增加）減少:' + str(cash_flow.decrease_increase_in_other_receivable_due_from_related_parties))
						elif r'存貨（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_inventories and symbolSeason2.decrease_increase_in_inventories and symbolSeason3.decrease_increase_in_inventories:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_inventories - symbolSeason2.decrease_increase_in_inventories - symbolSeason3.decrease_increase_in_inventories
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_inventories and symbolSeason3.decrease_increase_in_inventories:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_inventories - symbolSeason3.decrease_increase_in_inventories
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_inventories:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_inventories
									else:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_inventories and symbolSeason2.decrease_increase_in_inventories:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_inventories - symbolSeason2.decrease_increase_in_inventories
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_inventories:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_inventories
									else:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_inventories:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_inventories
									else:
										cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string)
								# print('存貨（增加）減少:' + str(cash_flow.decrease_increase_in_inventories))
						elif r'預付款項（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_prepayments and symbolSeason2.decrease_increase_in_prepayments and symbolSeason3.decrease_increase_in_prepayments:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_prepayments - symbolSeason2.decrease_increase_in_prepayments - symbolSeason3.decrease_increase_in_prepayments
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_prepayments and symbolSeason3.decrease_increase_in_prepayments:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_prepayments - symbolSeason3.decrease_increase_in_prepayments
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_prepayments:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_prepayments
									else:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_prepayments and symbolSeason2.decrease_increase_in_prepayments:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_prepayments - symbolSeason2.decrease_increase_in_prepayments
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_prepayments:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_prepayments
									else:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_prepayments:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_prepayments
									else:
										cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string)
								# print('預付款項（增加）減少:' + str(cash_flow.decrease_increase_in_prepayments))
						elif r'其他流動資產（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_other_current_assets and symbolSeason2.decrease_increase_in_other_current_assets and symbolSeason3.decrease_increase_in_other_current_assets:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_current_assets - symbolSeason2.decrease_increase_in_other_current_assets - symbolSeason3.decrease_increase_in_other_current_assets
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_other_current_assets and symbolSeason3.decrease_increase_in_other_current_assets:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_other_current_assets - symbolSeason3.decrease_increase_in_other_current_assets
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_other_current_assets:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_other_current_assets
									else:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_other_current_assets and symbolSeason2.decrease_increase_in_other_current_assets:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_current_assets - symbolSeason2.decrease_increase_in_other_current_assets
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_other_current_assets:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_other_current_assets
									else:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_other_current_assets:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_current_assets
									else:
										cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string)
								# print('其他流動資產（增加）減少:' + str(cash_flow.decrease_increase_in_other_current_assets))
						elif r'其他金融資產（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_other_financial_assets and symbolSeason2.decrease_increase_in_other_financial_assets and symbolSeason3.decrease_increase_in_other_financial_assets:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_financial_assets - symbolSeason2.decrease_increase_in_other_financial_assets - symbolSeason3.decrease_increase_in_other_financial_assets
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_other_financial_assets and symbolSeason3.decrease_increase_in_other_financial_assets:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_other_financial_assets - symbolSeason3.decrease_increase_in_other_financial_assets
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_other_financial_assets:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_other_financial_assets
									else:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_other_financial_assets and symbolSeason2.decrease_increase_in_other_financial_assets:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_financial_assets - symbolSeason2.decrease_increase_in_other_financial_assets
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_other_financial_assets:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_other_financial_assets
									else:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_other_financial_assets:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_financial_assets
									else:
										cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string)
								# print('其他金融資產（增加）減少:' + str(cash_flow.decrease_increase_in_other_financial_assets))
						elif r'其他營業資產（增加）減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_increase_in_other_operating_assets and symbolSeason2.decrease_increase_in_other_operating_assets and symbolSeason3.decrease_increase_in_other_operating_assets:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_operating_assets - symbolSeason2.decrease_increase_in_other_operating_assets - symbolSeason3.decrease_increase_in_other_operating_assets
									elif has_2_PrevSeasons and symbolSeason2.decrease_increase_in_other_operating_assets and symbolSeason3.decrease_increase_in_other_operating_assets:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_other_operating_assets - symbolSeason3.decrease_increase_in_other_operating_assets
									elif has_1_PrevSeasons and symbolSeason3.decrease_increase_in_other_operating_assets:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string) - symbolSeason3.decrease_increase_in_other_operating_assets
									else:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_increase_in_other_operating_assets and symbolSeason2.decrease_increase_in_other_operating_assets:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_operating_assets - symbolSeason2.decrease_increase_in_other_operating_assets
									elif has_1_PrevSeasons and symbolSeason2.decrease_increase_in_other_operating_assets:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string) - symbolSeason2.decrease_increase_in_other_operating_assets
									else:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_increase_in_other_operating_assets:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string) - symbolSeason1.decrease_increase_in_other_operating_assets
									else:
										cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string)
								# print('其他營業資產（增加）減少:' + str(cash_flow.decrease_increase_in_other_operating_assets))
						elif r'與營業活動相關之資產之淨變動合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.total_changes_in_operating_assets and symbolSeason2.total_changes_in_operating_assets and symbolSeason3.total_changes_in_operating_assets:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_assets - symbolSeason2.total_changes_in_operating_assets - symbolSeason3.total_changes_in_operating_assets
									elif has_2_PrevSeasons and symbolSeason2.total_changes_in_operating_assets and symbolSeason3.total_changes_in_operating_assets:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string) - symbolSeason2.total_changes_in_operating_assets - symbolSeason3.total_changes_in_operating_assets
									elif has_1_PrevSeasons and symbolSeason3.total_changes_in_operating_assets:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string) - symbolSeason3.total_changes_in_operating_assets
									else:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.total_changes_in_operating_assets and symbolSeason2.total_changes_in_operating_assets:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_assets - symbolSeason2.total_changes_in_operating_assets
									elif has_1_PrevSeasons and symbolSeason2.total_changes_in_operating_assets:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string) - symbolSeason2.total_changes_in_operating_assets
									else:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.total_changes_in_operating_assets:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_assets
									else:
										cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string)
								# print('與營業活動相關之資產之淨變動合計:' + str(cash_flow.total_changes_in_operating_assets))
						elif r'應付帳款增加（減少）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_decrease_in_accounts_payable and symbolSeason2.increase_decrease_in_accounts_payable and symbolSeason3.increase_decrease_in_accounts_payable:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accounts_payable - symbolSeason2.increase_decrease_in_accounts_payable - symbolSeason3.increase_decrease_in_accounts_payable
									elif has_2_PrevSeasons and symbolSeason2.increase_decrease_in_accounts_payable and symbolSeason3.increase_decrease_in_accounts_payable:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_accounts_payable - symbolSeason3.increase_decrease_in_accounts_payable
									elif has_1_PrevSeasons and symbolSeason3.increase_decrease_in_accounts_payable:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string) - symbolSeason3.increase_decrease_in_accounts_payable
									else:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_decrease_in_accounts_payable and symbolSeason2.increase_decrease_in_accounts_payable:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accounts_payable - symbolSeason2.increase_decrease_in_accounts_payable
									elif has_1_PrevSeasons and symbolSeason2.increase_decrease_in_accounts_payable:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_accounts_payable
									else:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_decrease_in_accounts_payable:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accounts_payable
									else:
										cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string)
								# print('應付帳款增加（減少）:' + str(cash_flow.increase_decrease_in_accounts_payable))
						elif r'應付帳款－關係人增加（減少）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_decrease_in_accounts_payable_to_related_parties and symbolSeason2.increase_decrease_in_accounts_payable_to_related_parties and symbolSeason3.increase_decrease_in_accounts_payable_to_related_parties:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accounts_payable_to_related_parties - symbolSeason2.increase_decrease_in_accounts_payable_to_related_parties - symbolSeason3.increase_decrease_in_accounts_payable_to_related_parties
									elif has_2_PrevSeasons and symbolSeason2.increase_decrease_in_accounts_payable_to_related_parties and symbolSeason3.increase_decrease_in_accounts_payable_to_related_parties:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_accounts_payable_to_related_parties - symbolSeason3.increase_decrease_in_accounts_payable_to_related_parties
									elif has_1_PrevSeasons and symbolSeason3.increase_decrease_in_accounts_payable_to_related_parties:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string) - symbolSeason3.increase_decrease_in_accounts_payable_to_related_parties
									else:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_decrease_in_accounts_payable_to_related_parties and symbolSeason2.increase_decrease_in_accounts_payable_to_related_parties:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accounts_payable_to_related_parties - symbolSeason2.increase_decrease_in_accounts_payable_to_related_parties
									elif has_1_PrevSeasons and symbolSeason2.increase_decrease_in_accounts_payable_to_related_parties:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_accounts_payable_to_related_parties
									else:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_decrease_in_accounts_payable_to_related_parties:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accounts_payable_to_related_parties
									else:
										cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string)
								# print('應付帳款－關係人增加（減少）:' + str(cash_flow.increase_decrease_in_accounts_payable_to_related_parties))
						elif r'其他應付款增加（減少）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_decrease_in_other_payable and symbolSeason2.increase_decrease_in_other_payable and symbolSeason3.increase_decrease_in_other_payable:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_other_payable - symbolSeason2.increase_decrease_in_other_payable - symbolSeason3.increase_decrease_in_other_payable
									elif has_2_PrevSeasons and symbolSeason2.increase_decrease_in_other_payable and symbolSeason3.increase_decrease_in_other_payable:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_other_payable - symbolSeason3.increase_decrease_in_other_payable
									elif has_1_PrevSeasons and symbolSeason3.increase_decrease_in_other_payable:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string) - symbolSeason3.increase_decrease_in_other_payable
									else:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_decrease_in_other_payable and symbolSeason2.increase_decrease_in_other_payable:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_other_payable - symbolSeason2.increase_decrease_in_other_payable
									elif has_1_PrevSeasons and symbolSeason2.increase_decrease_in_other_payable:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_other_payable
									else:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_decrease_in_other_payable:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_other_payable
									else:
										cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string)
								# print('其他應付款增加（減少）:' + str(cash_flow.increase_decrease_in_other_payable))
						elif r'負債準備增加（減少）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_decrease_in_provisions and symbolSeason2.increase_decrease_in_provisions and symbolSeason3.increase_decrease_in_provisions:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_provisions - symbolSeason2.increase_decrease_in_provisions - symbolSeason3.increase_decrease_in_provisions
									elif has_2_PrevSeasons and symbolSeason2.increase_decrease_in_provisions and symbolSeason3.increase_decrease_in_provisions:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_provisions - symbolSeason3.increase_decrease_in_provisions
									elif has_1_PrevSeasons and symbolSeason3.increase_decrease_in_provisions:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string) - symbolSeason3.increase_decrease_in_provisions
									else:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_decrease_in_provisions and symbolSeason2.increase_decrease_in_provisions:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_provisions - symbolSeason2.increase_decrease_in_provisions
									elif has_1_PrevSeasons and symbolSeason2.increase_decrease_in_provisions:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_provisions
									else:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_decrease_in_provisions:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_provisions
									else:
										cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string)
								# print('負債準備增加（減少）:' + str(cash_flow.increase_decrease_in_provisions))
						elif r'其他流動負債增加（減少）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_decrease_in_other_current_liabilities and symbolSeason2.increase_decrease_in_other_current_liabilities and symbolSeason3.increase_decrease_in_other_current_liabilities:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_other_current_liabilities - symbolSeason2.increase_decrease_in_other_current_liabilities - symbolSeason3.increase_decrease_in_other_current_liabilities
									elif has_2_PrevSeasons and symbolSeason2.increase_decrease_in_other_current_liabilities and symbolSeason3.increase_decrease_in_other_current_liabilities:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_other_current_liabilities - symbolSeason3.increase_decrease_in_other_current_liabilities
									elif has_1_PrevSeasons and symbolSeason3.increase_decrease_in_other_current_liabilities:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string) - symbolSeason3.increase_decrease_in_other_current_liabilities
									else:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_decrease_in_other_current_liabilities and symbolSeason2.increase_decrease_in_other_current_liabilities:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_other_current_liabilities - symbolSeason2.increase_decrease_in_other_current_liabilities
									elif has_1_PrevSeasons and symbolSeason2.increase_decrease_in_other_current_liabilities:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_other_current_liabilities
									else:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_decrease_in_other_current_liabilities:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_other_current_liabilities
									else:
										cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string)
								# print('其他流動負債增加（減少）:' + str(cash_flow.increase_decrease_in_other_current_liabilities))
						elif r'應計退休金負債增加（減少）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_decrease_in_accrued_pension_liabilities and symbolSeason2.increase_decrease_in_accrued_pension_liabilities and symbolSeason3.increase_decrease_in_accrued_pension_liabilities:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accrued_pension_liabilities - symbolSeason2.increase_decrease_in_accrued_pension_liabilities - symbolSeason3.increase_decrease_in_accrued_pension_liabilities
									elif has_2_PrevSeasons and symbolSeason2.increase_decrease_in_accrued_pension_liabilities and symbolSeason3.increase_decrease_in_accrued_pension_liabilities:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_accrued_pension_liabilities - symbolSeason3.increase_decrease_in_accrued_pension_liabilities
									elif has_1_PrevSeasons and symbolSeason3.increase_decrease_in_accrued_pension_liabilities:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string) - symbolSeason3.increase_decrease_in_accrued_pension_liabilities
									else:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_decrease_in_accrued_pension_liabilities and symbolSeason2.increase_decrease_in_accrued_pension_liabilities:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accrued_pension_liabilities - symbolSeason2.increase_decrease_in_accrued_pension_liabilities
									elif has_1_PrevSeasons and symbolSeason2.increase_decrease_in_accrued_pension_liabilities:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string) - symbolSeason2.increase_decrease_in_accrued_pension_liabilities
									else:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_decrease_in_accrued_pension_liabilities:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string) - symbolSeason1.increase_decrease_in_accrued_pension_liabilities
									else:
										cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string)
								# print('應計退休金負債增加（減少）:' + str(cash_flow.increase_decrease_in_accrued_pension_liabilities))
						elif r'與營業活動相關之負債之淨變動合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.total_changes_in_operating_liabilities and symbolSeason2.total_changes_in_operating_liabilities and symbolSeason3.total_changes_in_operating_liabilities:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_liabilities - symbolSeason2.total_changes_in_operating_liabilities - symbolSeason3.total_changes_in_operating_liabilities
									elif has_2_PrevSeasons and symbolSeason2.total_changes_in_operating_liabilities and symbolSeason3.total_changes_in_operating_liabilities:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string) - symbolSeason2.total_changes_in_operating_liabilities - symbolSeason3.total_changes_in_operating_liabilities
									elif has_1_PrevSeasons and symbolSeason3.total_changes_in_operating_liabilities:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string) - symbolSeason3.total_changes_in_operating_liabilities
									else:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.total_changes_in_operating_liabilities and symbolSeason2.total_changes_in_operating_liabilities:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_liabilities - symbolSeason2.total_changes_in_operating_liabilities
									elif has_1_PrevSeasons and symbolSeason2.total_changes_in_operating_liabilities:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string) - symbolSeason2.total_changes_in_operating_liabilities
									else:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.total_changes_in_operating_liabilities:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_liabilities
									else:
										cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string)
								# print('與營業活動相關之負債之淨變動合計:' + str(cash_flow.total_changes_in_operating_liabilities))
						elif r'與營業活動相關之資產及負債之淨變動合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.total_changes_in_operating_assets_and_liabilities and symbolSeason2.total_changes_in_operating_assets_and_liabilities and symbolSeason3.total_changes_in_operating_assets_and_liabilities:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_assets_and_liabilities - symbolSeason2.total_changes_in_operating_assets_and_liabilities - symbolSeason3.total_changes_in_operating_assets_and_liabilities
									elif has_2_PrevSeasons and symbolSeason2.total_changes_in_operating_assets_and_liabilities and symbolSeason3.total_changes_in_operating_assets_and_liabilities:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string) - symbolSeason2.total_changes_in_operating_assets_and_liabilities - symbolSeason3.total_changes_in_operating_assets_and_liabilities
									elif has_1_PrevSeasons and symbolSeason3.total_changes_in_operating_assets_and_liabilities:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string) - symbolSeason3.total_changes_in_operating_assets_and_liabilities
									else:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.total_changes_in_operating_assets_and_liabilities and symbolSeason2.total_changes_in_operating_assets_and_liabilities:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_assets_and_liabilities - symbolSeason2.total_changes_in_operating_assets_and_liabilities
									elif has_1_PrevSeasons and symbolSeason2.total_changes_in_operating_assets_and_liabilities:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string) - symbolSeason2.total_changes_in_operating_assets_and_liabilities
									else:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.total_changes_in_operating_assets_and_liabilities:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string) - symbolSeason1.total_changes_in_operating_assets_and_liabilities
									else:
										cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string)
								# print('與營業活動相關之資產及負債之淨變動合計:' + str(cash_flow.total_changes_in_operating_assets_and_liabilities))
						elif r'調整項目合計' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.total_adjustments = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.total_adjustments and symbolSeason2.total_adjustments and symbolSeason3.total_adjustments:
										cash_flow.total_adjustments = string_to_decimal(next_data.string) - symbolSeason1.total_adjustments - symbolSeason2.total_adjustments - symbolSeason3.total_adjustments
									elif has_2_PrevSeasons and symbolSeason2.total_adjustments and symbolSeason3.total_adjustments:
										cash_flow.total_adjustments = string_to_decimal(next_data.string) - symbolSeason2.total_adjustments - symbolSeason3.total_adjustments
									elif has_1_PrevSeasons and symbolSeason3.total_adjustments:
										cash_flow.total_adjustments = string_to_decimal(next_data.string) - symbolSeason3.total_adjustments
									else:
										cash_flow.total_adjustments = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.total_adjustments and symbolSeason2.total_adjustments:
										cash_flow.total_adjustments = string_to_decimal(next_data.string) - symbolSeason1.total_adjustments - symbolSeason2.total_adjustments
									elif has_1_PrevSeasons and symbolSeason2.total_adjustments:
										cash_flow.total_adjustments = string_to_decimal(next_data.string) - symbolSeason2.total_adjustments
									else:
										cash_flow.total_adjustments = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.total_adjustments:
										cash_flow.total_adjustments = string_to_decimal(next_data.string) - symbolSeason1.total_adjustments
									else:
										cash_flow.total_adjustments = string_to_decimal(next_data.string)
								# print('調整項目合計:' + str(cash_flow.total_adjustments))
						elif r'營運產生之現金流入（流出）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.cash_inflow_outflow_generated_from_operations and symbolSeason2.cash_inflow_outflow_generated_from_operations and symbolSeason3.cash_inflow_outflow_generated_from_operations:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string) - symbolSeason1.cash_inflow_outflow_generated_from_operations - symbolSeason2.cash_inflow_outflow_generated_from_operations - symbolSeason3.cash_inflow_outflow_generated_from_operations
									elif has_2_PrevSeasons and symbolSeason2.cash_inflow_outflow_generated_from_operations and symbolSeason3.cash_inflow_outflow_generated_from_operations:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string) - symbolSeason2.cash_inflow_outflow_generated_from_operations - symbolSeason3.cash_inflow_outflow_generated_from_operations
									elif has_1_PrevSeasons and symbolSeason3.cash_inflow_outflow_generated_from_operations:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string) - symbolSeason3.cash_inflow_outflow_generated_from_operations
									else:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.cash_inflow_outflow_generated_from_operations and symbolSeason2.cash_inflow_outflow_generated_from_operations:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string) - symbolSeason1.cash_inflow_outflow_generated_from_operations - symbolSeason2.cash_inflow_outflow_generated_from_operations
									elif has_1_PrevSeasons and symbolSeason2.cash_inflow_outflow_generated_from_operations:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string) - symbolSeason2.cash_inflow_outflow_generated_from_operations
									else:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.cash_inflow_outflow_generated_from_operations:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string) - symbolSeason1.cash_inflow_outflow_generated_from_operations
									else:
										cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string)
								# print('營運產生之現金流入（流出）:' + str(cash_flow.cash_inflow_outflow_generated_from_operations))
						elif r'退還（支付）之所得稅' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.income_taxes_refund_paid and symbolSeason2.income_taxes_refund_paid and symbolSeason3.income_taxes_refund_paid:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string) - symbolSeason1.income_taxes_refund_paid - symbolSeason2.income_taxes_refund_paid - symbolSeason3.income_taxes_refund_paid
									elif has_2_PrevSeasons and symbolSeason2.income_taxes_refund_paid and symbolSeason3.income_taxes_refund_paid:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string) - symbolSeason2.income_taxes_refund_paid - symbolSeason3.income_taxes_refund_paid
									elif has_1_PrevSeasons and symbolSeason3.income_taxes_refund_paid:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string) - symbolSeason3.income_taxes_refund_paid
									else:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.income_taxes_refund_paid and symbolSeason2.income_taxes_refund_paid:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string) - symbolSeason1.income_taxes_refund_paid - symbolSeason2.income_taxes_refund_paid
									elif has_1_PrevSeasons and symbolSeason2.income_taxes_refund_paid:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string) - symbolSeason2.income_taxes_refund_paid
									else:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.income_taxes_refund_paid:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string) - symbolSeason1.income_taxes_refund_paid
									else:
										cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string)
								# print('退還（支付）之所得稅:' + str(cash_flow.income_taxes_refund_paid))
						elif r'營業活動之淨現金流入（流出）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_operating_activities and symbolSeason2.net_cash_flows_from_used_in_operating_activities and symbolSeason3.net_cash_flows_from_used_in_operating_activities:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_operating_activities - symbolSeason2.net_cash_flows_from_used_in_operating_activities - symbolSeason3.net_cash_flows_from_used_in_operating_activities
									elif has_2_PrevSeasons and symbolSeason2.net_cash_flows_from_used_in_operating_activities and symbolSeason3.net_cash_flows_from_used_in_operating_activities:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string) - symbolSeason2.net_cash_flows_from_used_in_operating_activities - symbolSeason3.net_cash_flows_from_used_in_operating_activities
									elif has_1_PrevSeasons and symbolSeason3.net_cash_flows_from_used_in_operating_activities:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string) - symbolSeason3.net_cash_flows_from_used_in_operating_activities
									else:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_operating_activities and symbolSeason2.net_cash_flows_from_used_in_operating_activities:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_operating_activities - symbolSeason2.net_cash_flows_from_used_in_operating_activities
									elif has_1_PrevSeasons and symbolSeason2.net_cash_flows_from_used_in_operating_activities:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string) - symbolSeason2.net_cash_flows_from_used_in_operating_activities
									else:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_operating_activities:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_operating_activities
									else:
										cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string)
								# print('營業活動之淨現金流入（流出）:' + str(cash_flow.net_cash_flows_from_used_in_operating_activities))
						elif r'取得備供出售金融資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.acquisition_of_available_for_sale_financial_assets and symbolSeason2.acquisition_of_available_for_sale_financial_assets and symbolSeason3.acquisition_of_available_for_sale_financial_assets:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_available_for_sale_financial_assets - symbolSeason2.acquisition_of_available_for_sale_financial_assets - symbolSeason3.acquisition_of_available_for_sale_financial_assets
									elif has_2_PrevSeasons and symbolSeason2.acquisition_of_available_for_sale_financial_assets and symbolSeason3.acquisition_of_available_for_sale_financial_assets:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.acquisition_of_available_for_sale_financial_assets - symbolSeason3.acquisition_of_available_for_sale_financial_assets
									elif has_1_PrevSeasons and symbolSeason3.acquisition_of_available_for_sale_financial_assets:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason3.acquisition_of_available_for_sale_financial_assets
									else:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.acquisition_of_available_for_sale_financial_assets and symbolSeason2.acquisition_of_available_for_sale_financial_assets:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_available_for_sale_financial_assets - symbolSeason2.acquisition_of_available_for_sale_financial_assets
									elif has_1_PrevSeasons and symbolSeason2.acquisition_of_available_for_sale_financial_assets:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.acquisition_of_available_for_sale_financial_assets
									else:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.acquisition_of_available_for_sale_financial_assets:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_available_for_sale_financial_assets
									else:
										cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								# print('取得備供出售金融資產:' + str(cash_flow.acquisition_of_available_for_sale_financial_assets))
						elif r'處分備供出售金融資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_available_for_sale_financial_assets and symbolSeason2.proceeds_from_disposal_of_available_for_sale_financial_assets and symbolSeason3.proceeds_from_disposal_of_available_for_sale_financial_assets:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_available_for_sale_financial_assets - symbolSeason2.proceeds_from_disposal_of_available_for_sale_financial_assets - symbolSeason3.proceeds_from_disposal_of_available_for_sale_financial_assets
									elif has_2_PrevSeasons and symbolSeason2.proceeds_from_disposal_of_available_for_sale_financial_assets and symbolSeason3.proceeds_from_disposal_of_available_for_sale_financial_assets:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_disposal_of_available_for_sale_financial_assets - symbolSeason3.proceeds_from_disposal_of_available_for_sale_financial_assets
									elif has_1_PrevSeasons and symbolSeason3.proceeds_from_disposal_of_available_for_sale_financial_assets:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason3.proceeds_from_disposal_of_available_for_sale_financial_assets
									else:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_available_for_sale_financial_assets and symbolSeason2.proceeds_from_disposal_of_available_for_sale_financial_assets:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_available_for_sale_financial_assets - symbolSeason2.proceeds_from_disposal_of_available_for_sale_financial_assets
									elif has_1_PrevSeasons and symbolSeason2.proceeds_from_disposal_of_available_for_sale_financial_assets:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_disposal_of_available_for_sale_financial_assets
									else:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_available_for_sale_financial_assets:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_available_for_sale_financial_assets
									else:
										cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
								# print('處分備供出售金融資產:' + str(cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets))
						elif r'持有至到期日金融資產到期還本' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.proceeds_from_repayments_of_held_to_maturity_financial_assets and symbolSeason2.proceeds_from_repayments_of_held_to_maturity_financial_assets and symbolSeason3.proceeds_from_repayments_of_held_to_maturity_financial_assets:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_repayments_of_held_to_maturity_financial_assets - symbolSeason2.proceeds_from_repayments_of_held_to_maturity_financial_assets - symbolSeason3.proceeds_from_repayments_of_held_to_maturity_financial_assets
									elif has_2_PrevSeasons and symbolSeason2.proceeds_from_repayments_of_held_to_maturity_financial_assets and symbolSeason3.proceeds_from_repayments_of_held_to_maturity_financial_assets:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_repayments_of_held_to_maturity_financial_assets - symbolSeason3.proceeds_from_repayments_of_held_to_maturity_financial_assets
									elif has_1_PrevSeasons and symbolSeason3.proceeds_from_repayments_of_held_to_maturity_financial_assets:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string) - symbolSeason3.proceeds_from_repayments_of_held_to_maturity_financial_assets
									else:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.proceeds_from_repayments_of_held_to_maturity_financial_assets and symbolSeason2.proceeds_from_repayments_of_held_to_maturity_financial_assets:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_repayments_of_held_to_maturity_financial_assets - symbolSeason2.proceeds_from_repayments_of_held_to_maturity_financial_assets
									elif has_1_PrevSeasons and symbolSeason2.proceeds_from_repayments_of_held_to_maturity_financial_assets:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_repayments_of_held_to_maturity_financial_assets
									else:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.proceeds_from_repayments_of_held_to_maturity_financial_assets:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_repayments_of_held_to_maturity_financial_assets
									else:
										cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string)
								# print('持有至到期日金融資產到期還本:' + str(cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets))
						elif r'取得以成本衡量之金融資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.acquisition_of_financial_assets_at_cost and symbolSeason2.acquisition_of_financial_assets_at_cost and symbolSeason3.acquisition_of_financial_assets_at_cost:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_financial_assets_at_cost - symbolSeason2.acquisition_of_financial_assets_at_cost - symbolSeason3.acquisition_of_financial_assets_at_cost
									elif has_2_PrevSeasons and symbolSeason2.acquisition_of_financial_assets_at_cost and symbolSeason3.acquisition_of_financial_assets_at_cost:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason2.acquisition_of_financial_assets_at_cost - symbolSeason3.acquisition_of_financial_assets_at_cost
									elif has_1_PrevSeasons and symbolSeason3.acquisition_of_financial_assets_at_cost:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason3.acquisition_of_financial_assets_at_cost
									else:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.acquisition_of_financial_assets_at_cost and symbolSeason2.acquisition_of_financial_assets_at_cost:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_financial_assets_at_cost - symbolSeason2.acquisition_of_financial_assets_at_cost
									elif has_1_PrevSeasons and symbolSeason2.acquisition_of_financial_assets_at_cost:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason2.acquisition_of_financial_assets_at_cost
									else:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.acquisition_of_financial_assets_at_cost:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_financial_assets_at_cost
									else:
										cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string)
								# print('取得以成本衡量之金融資產:' + str(cash_flow.acquisition_of_financial_assets_at_cost))
						elif r'處分以成本衡量之金融資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_financial_assets_at_cost and symbolSeason2.proceeds_from_disposal_of_financial_assets_at_cost and symbolSeason3.proceeds_from_disposal_of_financial_assets_at_cost:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_financial_assets_at_cost - symbolSeason2.proceeds_from_disposal_of_financial_assets_at_cost - symbolSeason3.proceeds_from_disposal_of_financial_assets_at_cost
									elif has_2_PrevSeasons and symbolSeason2.proceeds_from_disposal_of_financial_assets_at_cost and symbolSeason3.proceeds_from_disposal_of_financial_assets_at_cost:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_disposal_of_financial_assets_at_cost - symbolSeason3.proceeds_from_disposal_of_financial_assets_at_cost
									elif has_1_PrevSeasons and symbolSeason3.proceeds_from_disposal_of_financial_assets_at_cost:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason3.proceeds_from_disposal_of_financial_assets_at_cost
									else:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_financial_assets_at_cost and symbolSeason2.proceeds_from_disposal_of_financial_assets_at_cost:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_financial_assets_at_cost - symbolSeason2.proceeds_from_disposal_of_financial_assets_at_cost
									elif has_1_PrevSeasons and symbolSeason2.proceeds_from_disposal_of_financial_assets_at_cost:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_disposal_of_financial_assets_at_cost
									else:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_financial_assets_at_cost:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_financial_assets_at_cost
									else:
										cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string)
								# print('處分以成本衡量之金融資產:' + str(cash_flow.proceeds_from_disposal_of_financial_assets_at_cost))
						elif r'取得不動產、廠房及設備' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.acquisition_of_property_plant_and_equipment and symbolSeason2.acquisition_of_property_plant_and_equipment and symbolSeason3.acquisition_of_property_plant_and_equipment:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_property_plant_and_equipment - symbolSeason2.acquisition_of_property_plant_and_equipment - symbolSeason3.acquisition_of_property_plant_and_equipment
									elif has_2_PrevSeasons and symbolSeason2.acquisition_of_property_plant_and_equipment and symbolSeason3.acquisition_of_property_plant_and_equipment:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason2.acquisition_of_property_plant_and_equipment - symbolSeason3.acquisition_of_property_plant_and_equipment
									elif has_1_PrevSeasons and symbolSeason3.acquisition_of_property_plant_and_equipment:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason3.acquisition_of_property_plant_and_equipment
									else:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.acquisition_of_property_plant_and_equipment and symbolSeason2.acquisition_of_property_plant_and_equipment:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_property_plant_and_equipment - symbolSeason2.acquisition_of_property_plant_and_equipment
									elif has_1_PrevSeasons and symbolSeason2.acquisition_of_property_plant_and_equipment:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason2.acquisition_of_property_plant_and_equipment
									else:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.acquisition_of_property_plant_and_equipment:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_property_plant_and_equipment
									else:
										cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string)
								# print('取得不動產、廠房及設備:' + str(cash_flow.acquisition_of_property_plant_and_equipment))
						elif r'處分不動產、廠房及設備' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_property_plant_and_equipment and symbolSeason2.proceeds_from_disposal_of_property_plant_and_equipment and symbolSeason3.proceeds_from_disposal_of_property_plant_and_equipment:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_property_plant_and_equipment - symbolSeason2.proceeds_from_disposal_of_property_plant_and_equipment - symbolSeason3.proceeds_from_disposal_of_property_plant_and_equipment
									elif has_2_PrevSeasons and symbolSeason2.proceeds_from_disposal_of_property_plant_and_equipment and symbolSeason3.proceeds_from_disposal_of_property_plant_and_equipment:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_disposal_of_property_plant_and_equipment - symbolSeason3.proceeds_from_disposal_of_property_plant_and_equipment
									elif has_1_PrevSeasons and symbolSeason3.proceeds_from_disposal_of_property_plant_and_equipment:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason3.proceeds_from_disposal_of_property_plant_and_equipment
									else:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_property_plant_and_equipment and symbolSeason2.proceeds_from_disposal_of_property_plant_and_equipment:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_property_plant_and_equipment - symbolSeason2.proceeds_from_disposal_of_property_plant_and_equipment
									elif has_1_PrevSeasons and symbolSeason2.proceeds_from_disposal_of_property_plant_and_equipment:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_disposal_of_property_plant_and_equipment
									else:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.proceeds_from_disposal_of_property_plant_and_equipment:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_disposal_of_property_plant_and_equipment
									else:
										cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string)
								# print('處分不動產、廠房及設備:' + str(cash_flow.proceeds_from_disposal_of_property_plant_and_equipment))						
						elif r'取得無形資產' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.acquisition_of_intangible_assets and symbolSeason2.acquisition_of_intangible_assets and symbolSeason3.acquisition_of_intangible_assets:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_intangible_assets - symbolSeason2.acquisition_of_intangible_assets - symbolSeason3.acquisition_of_intangible_assets
									elif has_2_PrevSeasons and symbolSeason2.acquisition_of_intangible_assets and symbolSeason3.acquisition_of_intangible_assets:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string) - symbolSeason2.acquisition_of_intangible_assets - symbolSeason3.acquisition_of_intangible_assets
									elif has_1_PrevSeasons and symbolSeason3.acquisition_of_intangible_assets:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string) - symbolSeason3.acquisition_of_intangible_assets
									else:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.acquisition_of_intangible_assets and symbolSeason2.acquisition_of_intangible_assets:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_intangible_assets - symbolSeason2.acquisition_of_intangible_assets
									elif has_1_PrevSeasons and symbolSeason2.acquisition_of_intangible_assets:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string) - symbolSeason2.acquisition_of_intangible_assets
									else:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.acquisition_of_intangible_assets:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string) - symbolSeason1.acquisition_of_intangible_assets
									else:
										cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string)
								# print('取得無形資產:' + str(cash_flow.acquisition_of_intangible_assets))
						elif r'其他非流動資產增加' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_in_other_non_current_assets and symbolSeason2.increase_in_other_non_current_assets and symbolSeason3.increase_in_other_non_current_assets:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string) - symbolSeason1.increase_in_other_non_current_assets - symbolSeason2.increase_in_other_non_current_assets - symbolSeason3.increase_in_other_non_current_assets
									elif has_2_PrevSeasons and symbolSeason2.increase_in_other_non_current_assets and symbolSeason3.increase_in_other_non_current_assets:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string) - symbolSeason2.increase_in_other_non_current_assets - symbolSeason3.increase_in_other_non_current_assets
									elif has_1_PrevSeasons and symbolSeason3.increase_in_other_non_current_assets:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string) - symbolSeason3.increase_in_other_non_current_assets
									else:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_in_other_non_current_assets and symbolSeason2.increase_in_other_non_current_assets:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string) - symbolSeason1.increase_in_other_non_current_assets - symbolSeason2.increase_in_other_non_current_assets
									elif has_1_PrevSeasons and symbolSeason2.increase_in_other_non_current_assets:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string) - symbolSeason2.increase_in_other_non_current_assets
									else:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_in_other_non_current_assets:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string) - symbolSeason1.increase_in_other_non_current_assets
									else:
										cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string)
								# print('其他非流動資產增加:' + str(cash_flow.increase_in_other_non_current_assets))
						elif r'投資活動之淨現金流入（流出）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_investing_activities and symbolSeason2.net_cash_flows_from_used_in_investing_activities and symbolSeason3.net_cash_flows_from_used_in_investing_activities:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_investing_activities - symbolSeason2.net_cash_flows_from_used_in_investing_activities - symbolSeason3.net_cash_flows_from_used_in_investing_activities
									elif has_2_PrevSeasons and symbolSeason2.net_cash_flows_from_used_in_investing_activities and symbolSeason3.net_cash_flows_from_used_in_investing_activities:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string) - symbolSeason2.net_cash_flows_from_used_in_investing_activities - symbolSeason3.net_cash_flows_from_used_in_investing_activities
									elif has_1_PrevSeasons and symbolSeason3.net_cash_flows_from_used_in_investing_activities:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string) - symbolSeason3.net_cash_flows_from_used_in_investing_activities
									else:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_investing_activities and symbolSeason2.net_cash_flows_from_used_in_investing_activities:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_investing_activities - symbolSeason2.net_cash_flows_from_used_in_investing_activities
									elif has_1_PrevSeasons and symbolSeason2.net_cash_flows_from_used_in_investing_activities:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string) - symbolSeason2.net_cash_flows_from_used_in_investing_activities
									else:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_investing_activities:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_investing_activities
									else:
										cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string)
								# print('投資活動之淨現金流入（流出）:' + str(cash_flow.net_cash_flows_from_used_in_investing_activities))
						elif r'短期借款增加' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_in_short_term_loans and symbolSeason2.increase_in_short_term_loans and symbolSeason3.increase_in_short_term_loans:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason1.increase_in_short_term_loans - symbolSeason2.increase_in_short_term_loans - symbolSeason3.increase_in_short_term_loans
									elif has_2_PrevSeasons and symbolSeason2.increase_in_short_term_loans and symbolSeason3.increase_in_short_term_loans:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason2.increase_in_short_term_loans - symbolSeason3.increase_in_short_term_loans
									elif has_1_PrevSeasons and symbolSeason3.increase_in_short_term_loans:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason3.increase_in_short_term_loans
									else:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_in_short_term_loans and symbolSeason2.increase_in_short_term_loans:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason1.increase_in_short_term_loans - symbolSeason2.increase_in_short_term_loans
									elif has_1_PrevSeasons and symbolSeason2.increase_in_short_term_loans:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason2.increase_in_short_term_loans
									else:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_in_short_term_loans:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason1.increase_in_short_term_loans
									else:
										cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string)
								# print('短期借款增加:' + str(cash_flow.increase_in_short_term_loans))
						elif r'短期借款減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_in_short_term_loans and symbolSeason2.decrease_in_short_term_loans and symbolSeason3.decrease_in_short_term_loans:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason1.decrease_in_short_term_loans - symbolSeason2.decrease_in_short_term_loans - symbolSeason3.decrease_in_short_term_loans
									elif has_2_PrevSeasons and symbolSeason2.decrease_in_short_term_loans and symbolSeason3.decrease_in_short_term_loans:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason2.decrease_in_short_term_loans - symbolSeason3.decrease_in_short_term_loans
									elif has_1_PrevSeasons and symbolSeason3.decrease_in_short_term_loans:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason3.decrease_in_short_term_loans
									else:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_in_short_term_loans and symbolSeason2.decrease_in_short_term_loans:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason1.decrease_in_short_term_loans - symbolSeason2.decrease_in_short_term_loans
									elif has_1_PrevSeasons and symbolSeason2.decrease_in_short_term_loans:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason2.decrease_in_short_term_loans
									else:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_in_short_term_loans:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string) - symbolSeason1.decrease_in_short_term_loans
									else:
										cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string)
								# print('短期借款減少:' + str(cash_flow.decrease_in_short_term_loans))
						elif r'應付短期票券增加' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.increase_in_short_term_notes_and_bills_payable and symbolSeason2.increase_in_short_term_notes_and_bills_payable and symbolSeason3.increase_in_short_term_notes_and_bills_payable:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_in_short_term_notes_and_bills_payable - symbolSeason2.increase_in_short_term_notes_and_bills_payable - symbolSeason3.increase_in_short_term_notes_and_bills_payable
									elif has_2_PrevSeasons and symbolSeason2.increase_in_short_term_notes_and_bills_payable and symbolSeason3.increase_in_short_term_notes_and_bills_payable:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason2.increase_in_short_term_notes_and_bills_payable - symbolSeason3.increase_in_short_term_notes_and_bills_payable
									elif has_1_PrevSeasons and symbolSeason3.increase_in_short_term_notes_and_bills_payable:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason3.increase_in_short_term_notes_and_bills_payable
									else:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.increase_in_short_term_notes_and_bills_payable and symbolSeason2.increase_in_short_term_notes_and_bills_payable:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_in_short_term_notes_and_bills_payable - symbolSeason2.increase_in_short_term_notes_and_bills_payable
									elif has_1_PrevSeasons and symbolSeason2.increase_in_short_term_notes_and_bills_payable:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason2.increase_in_short_term_notes_and_bills_payable
									else:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.increase_in_short_term_notes_and_bills_payable:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason1.increase_in_short_term_notes_and_bills_payable
									else:
										cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								# print('應付短期票券增加:' + str(cash_flow.increase_in_short_term_notes_and_bills_payable))
						elif r'應付短期票券減少' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.decrease_in_short_term_notes_and_bills_payable and symbolSeason2.decrease_in_short_term_notes_and_bills_payable and symbolSeason3.decrease_in_short_term_notes_and_bills_payable:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason1.decrease_in_short_term_notes_and_bills_payable - symbolSeason2.decrease_in_short_term_notes_and_bills_payable - symbolSeason3.decrease_in_short_term_notes_and_bills_payable
									elif has_2_PrevSeasons and symbolSeason2.decrease_in_short_term_notes_and_bills_payable and symbolSeason3.decrease_in_short_term_notes_and_bills_payable:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason2.decrease_in_short_term_notes_and_bills_payable - symbolSeason3.decrease_in_short_term_notes_and_bills_payable
									elif has_1_PrevSeasons and symbolSeason3.decrease_in_short_term_notes_and_bills_payable:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason3.decrease_in_short_term_notes_and_bills_payable
									else:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.decrease_in_short_term_notes_and_bills_payable and symbolSeason2.decrease_in_short_term_notes_and_bills_payable:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason1.decrease_in_short_term_notes_and_bills_payable - symbolSeason2.decrease_in_short_term_notes_and_bills_payable
									elif has_1_PrevSeasons and symbolSeason2.decrease_in_short_term_notes_and_bills_payable:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason2.decrease_in_short_term_notes_and_bills_payable
									else:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.decrease_in_short_term_notes_and_bills_payable:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string) - symbolSeason1.decrease_in_short_term_notes_and_bills_payable
									else:
										cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
								# print('應付短期票券減少:' + str(cash_flow.decrease_in_short_term_notes_and_bills_payable))
						elif r'發行公司債' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.proceeds_from_issuing_bonds and symbolSeason2.proceeds_from_issuing_bonds and symbolSeason3.proceeds_from_issuing_bonds:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_issuing_bonds - symbolSeason2.proceeds_from_issuing_bonds - symbolSeason3.proceeds_from_issuing_bonds
									elif has_2_PrevSeasons and symbolSeason2.proceeds_from_issuing_bonds and symbolSeason3.proceeds_from_issuing_bonds:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_issuing_bonds - symbolSeason3.proceeds_from_issuing_bonds
									elif has_1_PrevSeasons and symbolSeason3.proceeds_from_issuing_bonds:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string) - symbolSeason3.proceeds_from_issuing_bonds
									else:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.proceeds_from_issuing_bonds and symbolSeason2.proceeds_from_issuing_bonds:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_issuing_bonds - symbolSeason2.proceeds_from_issuing_bonds
									elif has_1_PrevSeasons and symbolSeason2.proceeds_from_issuing_bonds:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_issuing_bonds
									else:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.proceeds_from_issuing_bonds:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_issuing_bonds
									else:
										cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string)
								# print('發行公司債:' + str(cash_flow.proceeds_from_issuing_bonds))
						elif r'償還公司債' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.repayments_of_bonds = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.repayments_of_bonds and symbolSeason2.repayments_of_bonds and symbolSeason3.repayments_of_bonds:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string) - symbolSeason1.repayments_of_bonds - symbolSeason2.repayments_of_bonds - symbolSeason3.repayments_of_bonds
									elif has_2_PrevSeasons and symbolSeason2.repayments_of_bonds and symbolSeason3.repayments_of_bonds:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string) - symbolSeason2.repayments_of_bonds - symbolSeason3.repayments_of_bonds
									elif has_1_PrevSeasons and symbolSeason3.repayments_of_bonds:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string) - symbolSeason3.repayments_of_bonds
									else:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.repayments_of_bonds and symbolSeason2.repayments_of_bonds:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string) - symbolSeason1.repayments_of_bonds - symbolSeason2.repayments_of_bonds
									elif has_1_PrevSeasons and symbolSeason2.repayments_of_bonds:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string) - symbolSeason2.repayments_of_bonds
									else:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.repayments_of_bonds:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string) - symbolSeason1.repayments_of_bonds
									else:
										cash_flow.repayments_of_bonds = string_to_decimal(next_data.string)
								# print('償還公司債:' + str(cash_flow.repayments_of_bonds))
						elif r'舉借長期借款' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.proceeds_from_long_term_debt and symbolSeason2.proceeds_from_long_term_debt and symbolSeason3.proceeds_from_long_term_debt:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_long_term_debt - symbolSeason2.proceeds_from_long_term_debt - symbolSeason3.proceeds_from_long_term_debt
									elif has_2_PrevSeasons and symbolSeason2.proceeds_from_long_term_debt and symbolSeason3.proceeds_from_long_term_debt:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_long_term_debt - symbolSeason3.proceeds_from_long_term_debt
									elif has_1_PrevSeasons and symbolSeason3.proceeds_from_long_term_debt:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string) - symbolSeason3.proceeds_from_long_term_debt
									else:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.proceeds_from_long_term_debt and symbolSeason2.proceeds_from_long_term_debt:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_long_term_debt - symbolSeason2.proceeds_from_long_term_debt
									elif has_1_PrevSeasons and symbolSeason2.proceeds_from_long_term_debt:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_long_term_debt
									else:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.proceeds_from_long_term_debt:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_long_term_debt
									else:
										cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string)
								# print('舉借長期借款:' + str(cash_flow.proceeds_from_long_term_debt))
						elif r'償還長期借款' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.repayments_of_long_term_debt and symbolSeason2.repayments_of_long_term_debt and symbolSeason3.repayments_of_long_term_debt:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string) - symbolSeason1.repayments_of_long_term_debt - symbolSeason2.repayments_of_long_term_debt - symbolSeason3.repayments_of_long_term_debt
									elif has_2_PrevSeasons and symbolSeason2.repayments_of_long_term_debt and symbolSeason3.repayments_of_long_term_debt:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string) - symbolSeason2.repayments_of_long_term_debt - symbolSeason3.repayments_of_long_term_debt
									elif has_1_PrevSeasons and symbolSeason3.repayments_of_long_term_debt:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string) - symbolSeason3.repayments_of_long_term_debt
									else:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.repayments_of_long_term_debt and symbolSeason2.repayments_of_long_term_debt:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string) - symbolSeason1.repayments_of_long_term_debt - symbolSeason2.repayments_of_long_term_debt
									elif has_1_PrevSeasons and symbolSeason2.repayments_of_long_term_debt:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string) - symbolSeason2.repayments_of_long_term_debt
									else:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.repayments_of_long_term_debt:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string) - symbolSeason1.repayments_of_long_term_debt
									else:
										cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string)
								# print('償還長期借款:' + str(cash_flow.repayments_of_long_term_debt))
						elif r'庫藏股票買回成本' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.payments_to_acquire_treasury_shares and symbolSeason2.payments_to_acquire_treasury_shares and symbolSeason3.payments_to_acquire_treasury_shares:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string) - symbolSeason1.payments_to_acquire_treasury_shares - symbolSeason2.payments_to_acquire_treasury_shares - symbolSeason3.payments_to_acquire_treasury_shares
									elif has_2_PrevSeasons and symbolSeason2.payments_to_acquire_treasury_shares and symbolSeason3.payments_to_acquire_treasury_shares:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string) - symbolSeason2.payments_to_acquire_treasury_shares - symbolSeason3.payments_to_acquire_treasury_shares
									elif has_1_PrevSeasons and symbolSeason3.payments_to_acquire_treasury_shares:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string) - symbolSeason3.payments_to_acquire_treasury_shares
									else:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.payments_to_acquire_treasury_shares and symbolSeason2.payments_to_acquire_treasury_shares:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string) - symbolSeason1.payments_to_acquire_treasury_shares - symbolSeason2.payments_to_acquire_treasury_shares
									elif has_1_PrevSeasons and symbolSeason2.payments_to_acquire_treasury_shares:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string) - symbolSeason2.payments_to_acquire_treasury_shares
									else:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.payments_to_acquire_treasury_shares:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string) - symbolSeason1.payments_to_acquire_treasury_shares
									else:
										cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string)
								# print('庫藏股票買回成本:' + str(cash_flow.payments_to_acquire_treasury_shares))
						elif r'庫藏股票處分' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.proceeds_from_sale_of_treasury_shares and symbolSeason2.proceeds_from_sale_of_treasury_shares and symbolSeason3.proceeds_from_sale_of_treasury_shares:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_sale_of_treasury_shares - symbolSeason2.proceeds_from_sale_of_treasury_shares - symbolSeason3.proceeds_from_sale_of_treasury_shares
									elif has_2_PrevSeasons and symbolSeason2.proceeds_from_sale_of_treasury_shares and symbolSeason3.proceeds_from_sale_of_treasury_shares:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_sale_of_treasury_shares - symbolSeason3.proceeds_from_sale_of_treasury_shares
									elif has_1_PrevSeasons and symbolSeason3.proceeds_from_sale_of_treasury_shares:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string) - symbolSeason3.proceeds_from_sale_of_treasury_shares
									else:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.proceeds_from_sale_of_treasury_shares and symbolSeason2.proceeds_from_sale_of_treasury_shares:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_sale_of_treasury_shares - symbolSeason2.proceeds_from_sale_of_treasury_shares
									elif has_1_PrevSeasons and symbolSeason2.proceeds_from_sale_of_treasury_shares:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string) - symbolSeason2.proceeds_from_sale_of_treasury_shares
									else:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.proceeds_from_sale_of_treasury_shares:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string) - symbolSeason1.proceeds_from_sale_of_treasury_shares
									else:
										cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string)
								# print('庫藏股票處分:' + str(cash_flow.proceeds_from_sale_of_treasury_shares))
						elif r'發放現金股利' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.cash_dividends_paid = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.cash_dividends_paid and symbolSeason2.cash_dividends_paid and symbolSeason3.cash_dividends_paid:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string) - symbolSeason1.cash_dividends_paid - symbolSeason2.cash_dividends_paid - symbolSeason3.cash_dividends_paid
									elif has_2_PrevSeasons and symbolSeason2.cash_dividends_paid and symbolSeason3.cash_dividends_paid:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string) - symbolSeason2.cash_dividends_paid - symbolSeason3.cash_dividends_paid
									elif has_1_PrevSeasons and symbolSeason3.cash_dividends_paid:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string) - symbolSeason3.cash_dividends_paid
									else:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.cash_dividends_paid and symbolSeason2.cash_dividends_paid:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string) - symbolSeason1.cash_dividends_paid - symbolSeason2.cash_dividends_paid
									elif has_1_PrevSeasons and symbolSeason2.cash_dividends_paid:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string) - symbolSeason2.cash_dividends_paid
									else:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.cash_dividends_paid:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string) - symbolSeason1.cash_dividends_paid
									else:
										cash_flow.cash_dividends_paid = string_to_decimal(next_data.string)
								# print('發放現金股利:' + str(cash_flow.cash_dividends_paid))
						elif r'籌資活動之淨現金流入（流出）' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_financing_activities and symbolSeason2.net_cash_flows_from_used_in_financing_activities and symbolSeason3.net_cash_flows_from_used_in_financing_activities:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_financing_activities - symbolSeason2.net_cash_flows_from_used_in_financing_activities - symbolSeason3.net_cash_flows_from_used_in_financing_activities
									elif has_2_PrevSeasons and symbolSeason2.net_cash_flows_from_used_in_financing_activities and symbolSeason3.net_cash_flows_from_used_in_financing_activities:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string) - symbolSeason2.net_cash_flows_from_used_in_financing_activities - symbolSeason3.net_cash_flows_from_used_in_financing_activities
									elif has_1_PrevSeasons and symbolSeason3.net_cash_flows_from_used_in_financing_activities:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string) - symbolSeason3.net_cash_flows_from_used_in_financing_activities
									else:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_financing_activities and symbolSeason2.net_cash_flows_from_used_in_financing_activities:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_financing_activities - symbolSeason2.net_cash_flows_from_used_in_financing_activities
									elif has_1_PrevSeasons and symbolSeason2.net_cash_flows_from_used_in_financing_activities:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string) - symbolSeason2.net_cash_flows_from_used_in_financing_activities
									else:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.net_cash_flows_from_used_in_financing_activities:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string) - symbolSeason1.net_cash_flows_from_used_in_financing_activities
									else:
										cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string)
								# print('籌資活動之淨現金流入（流出）:' + str(cash_flow.net_cash_flows_from_used_in_financing_activities))
						elif r'匯率變動對現金及約當現金之影響' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents and symbolSeason2.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents and symbolSeason3.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason1.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents - symbolSeason2.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents - symbolSeason3.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents
									elif has_2_PrevSeasons and symbolSeason2.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents and symbolSeason3.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason2.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents - symbolSeason3.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents
									elif has_1_PrevSeasons and symbolSeason3.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason3.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents
									else:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents and symbolSeason2.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason1.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents - symbolSeason2.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents
									elif has_1_PrevSeasons and symbolSeason2.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason2.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents
									else:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason1.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents
									else:
										cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								# print('匯率變動對現金及約當現金之影響:' + str(cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents))
						elif r'本期現金及約當現金增加（減少）數' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								if qtr == 1:
									cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								elif qtr == 4:
									if has_3_PrevSeasons and symbolSeason1.net_increase_decrease_in_cash_and_cash_equivalents and symbolSeason2.net_increase_decrease_in_cash_and_cash_equivalents and symbolSeason3.net_increase_decrease_in_cash_and_cash_equivalents:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason1.net_increase_decrease_in_cash_and_cash_equivalents - symbolSeason2.net_increase_decrease_in_cash_and_cash_equivalents - symbolSeason3.net_increase_decrease_in_cash_and_cash_equivalents
									elif has_2_PrevSeasons and symbolSeason2.net_increase_decrease_in_cash_and_cash_equivalents and symbolSeason3.net_increase_decrease_in_cash_and_cash_equivalents:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason2.net_increase_decrease_in_cash_and_cash_equivalents - symbolSeason3.net_increase_decrease_in_cash_and_cash_equivalents
									elif has_1_PrevSeasons and symbolSeason3.net_increase_decrease_in_cash_and_cash_equivalents:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason3.net_increase_decrease_in_cash_and_cash_equivalents
									else:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								elif qtr == 3:
									if has_2_PrevSeasons and symbolSeason1.net_increase_decrease_in_cash_and_cash_equivalents and symbolSeason2.net_increase_decrease_in_cash_and_cash_equivalents:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason1.net_increase_decrease_in_cash_and_cash_equivalents - symbolSeason2.net_increase_decrease_in_cash_and_cash_equivalents
									elif has_1_PrevSeasons and symbolSeason2.net_increase_decrease_in_cash_and_cash_equivalents:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason2.net_increase_decrease_in_cash_and_cash_equivalents
									else:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								elif qtr == 2:
									if has_1_PrevSeasons and symbolSeason1.net_increase_decrease_in_cash_and_cash_equivalents:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string) - symbolSeason1.net_increase_decrease_in_cash_and_cash_equivalents
									else:
										cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string)
								# print('本期現金及約當現金增加（減少）數:' + str(cash_flow.net_increase_decrease_in_cash_and_cash_equivalents))
						elif r'期末現金及約當現金餘額' in data.string.encode('utf-8'):
							if data.next_sibling.next_sibling.string is not None:
								next_data = data.next_sibling.next_sibling
								cash_flow.cash_and_cash_equivalents_at_end_of_period = string_to_decimal(next_data.string)
								# print('期末現金及約當現金餘額:' + str(cash_flow.cash_and_cash_equivalents_at_end_of_period))
				cash_flow.free_cash_flow = 0
				if cash_flow.net_cash_flows_from_used_in_operating_activities != None:
					cash_flow.free_cash_flow = cash_flow.free_cash_flow + cash_flow.net_cash_flows_from_used_in_operating_activities
				if cash_flow.net_cash_flows_from_used_in_investing_activities != None:
					cash_flow.free_cash_flow = cash_flow.free_cash_flow + cash_flow.net_cash_flows_from_used_in_investing_activities
				# print('自由現金流量:' + str(cash_flow.free_cash_flow))

				response.close()
				# 確定有抓到本期稅前淨利（淨損）的值，才將該檔股票資料寫入資料表中
				if cash_flow.profit_loss_before_tax is not None:
					cash_flow.save()
					print(symbol + " updated.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ") @ " + str(datetime.now()))
				else:
					print(symbol + " no data.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")

	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name":"現金流量表(季)"})

# 現金流量表（年）
def annual_cash_flow(request):

	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()
	# c.execute('DELETE FROM stockfins_annualcashflow')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	# # 輸入西元年(時間參數改由最外層控制)
	# yr = 2014

	start_time = datetime.now()
	stockID_updated = get_stockID_updated(request)

	cash_flow = AnnualCashFlow()
	count = 0
	stocks = StockID.objects.all()[count:]
	countAll = stocks.count() # 計算全部需要更新的股票檔數

	for stock in stocks:
		symbol = stock.symbol
		mkt = stock.market
		count = count + 1
		# STEP1.跳過金融股
		if symbol[:2] == "28":
			continue
		# STEP2.檢查資料是否已經存在資料庫，如果「是」，就跳過此檔不更新，以節省時間
		id_test_exist = str(yr) + '-' + symbol
		if AnnualCashFlow.objects.filter(ID=id_test_exist):
			print(symbol + u"資料已存在資料庫.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ")")
			continue
		# STEP3.檢查該檔股票的財報是否已經在更新清單裡面，如果有才進行連線更新，沒有的話就跳過
		if symbol not in stockID_updated:
			print(symbol + u"網站資料尚未更新.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ")")
			continue
		# 先宣告所有報表項目
		cash_flow.ID = str(yr) + '-' + symbol
		cash_flow.symbol = symbol
		cash_flow.year = yr
		cash_flow.profit_loss_from_continuing_operations_before_tax = None
		cash_flow.profit_loss_before_tax = None
		cash_flow.depreciation_expense = None
		cash_flow.amortization_expense = None
		cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = None
		cash_flow.interest_expense = None
		cash_flow.interest_income = None
		cash_flow.share_based_payments = None
		cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = None
		cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = None
		cash_flow.loss_gain_on_disposal_of_investments = None
		cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = None
		cash_flow.realized_loss_profit_on_from_sales = None
		cash_flow.unrealized_foreign_exchange_loss_gain = None
		cash_flow.other_adjustments_to_reconcile_profit_loss = None
		cash_flow.total_adjustments_to_reconcile_profit_loss = None
		cash_flow.decrease_increase_in_financial_assets_held_for_trading = None
		cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = None
		cash_flow.decrease_increase_in_notes_receivable = None
		cash_flow.decrease_increase_in_accounts_receivable = None
		cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = None
		cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = None
		cash_flow.decrease_increase_in_inventories = None
		cash_flow.decrease_increase_in_prepayments = None
		cash_flow.decrease_increase_in_other_current_assets = None
		cash_flow.decrease_increase_in_other_financial_assets = None
		cash_flow.decrease_increase_in_other_operating_assets = None
		cash_flow.total_changes_in_operating_assets = None
		cash_flow.increase_decrease_in_accounts_payable = None
		cash_flow.increase_decrease_in_accounts_payable_to_related_parties = None
		cash_flow.increase_decrease_in_other_payable = None
		cash_flow.increase_decrease_in_provisions = None
		cash_flow.increase_decrease_in_other_current_liabilities = None
		cash_flow.increase_decrease_in_accrued_pension_liabilities = None
		cash_flow.total_changes_in_operating_liabilities = None
		cash_flow.total_changes_in_operating_assets_and_liabilities = None
		cash_flow.total_adjustments = None
		cash_flow.cash_inflow_outflow_generated_from_operations = None
		cash_flow.income_taxes_refund_paid = None
		cash_flow.net_cash_flows_from_used_in_operating_activities = None
		cash_flow.acquisition_of_available_for_sale_financial_assets = None
		cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = None
		cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = None
		cash_flow.acquisition_of_financial_assets_at_cost = None
		cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = None
		cash_flow.acquisition_of_property_plant_and_equipment = None
		cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = None
		cash_flow.acquisition_of_intangible_assets = None
		cash_flow.increase_in_other_non_current_assets = None
		cash_flow.net_cash_flows_from_used_in_investing_activities = None
		cash_flow.increase_in_short_term_loans = None
		cash_flow.decrease_in_short_term_loans = None
		cash_flow.increase_in_short_term_notes_and_bills_payable = None
		cash_flow.decrease_in_short_term_notes_and_bills_payable = None
		cash_flow.proceeds_from_issuing_bonds = None
		cash_flow.repayments_of_bonds = None
		cash_flow.proceeds_from_long_term_debt = None
		cash_flow.repayments_of_long_term_debt = None
		cash_flow.payments_to_acquire_treasury_shares = None
		cash_flow.proceeds_from_sale_of_treasury_shares = None
		cash_flow.cash_dividends_paid
		cash_flow.net_cash_flows_from_used_in_financing_activities = None
		cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = None
		cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = None
		cash_flow.cash_and_cash_equivalents_at_beginning_of_period = None
		cash_flow.cash_and_cash_equivalents_at_end_of_period = None
		cash_flow.cash_and_cash_equivalents_reported_in_the_statement_of_financial_position = None
		cash_flow.free_cash_flow = None

		# 公開資訊觀測站存放上市櫃公司綜合損益表的網址
		url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb05'
		values = {'encodeURIComponent': '1', 'step': '1', 'firstin': '1', 'off': '1',
					'keyword4': '', 'code1': '', 'TYPEK2': '', 'checkbtn': '',
					'queryName': 'co_id', 'TYPEK': 'all', 'isnew': 'false',
					'co_id': symbol, 'year': str(yr-1911), 'season': '04'}
		url_data = urllib.urlencode(values)
		headers = {'User-Agent': 'Mozilla/5.0'}
		req = urllib2.Request(url, url_data, headers)

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
			annual_cashflow_datas = soup.find_all('td', attrs = {'style':'text-align:left;white-space:nowrap;'})
			busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
			# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
			while (busy_msg is not None):
				response.close()
				print("Server busy, Re-connect in 20 sec.")
				time.sleep(20)
				headers = {'User-Agent': 'Mozilla/4.0'}
				req = urllib2.Request(url, url_data, headers)
				try:
					response = urllib2.urlopen(req)
					print("Re-connect URL now!")
				except URLError, e:
					if hasattr(e, "reason"):
						print(symbol + "(" + str(count) + '/' + str(countAll) + "). Reason:"), e.reason
					elif hasattr(e, "code"):
						print(symbol + "(" + str(count) + '/' + str(countAll) + "). Error code:"), e.reason
				else:
					soup = BeautifulSoup(response, from_encoding = 'utf-8')
					annual_cashflow_datas = soup.find_all('td', attrs = {'style':'text-align:left;white-space:nowrap;'})
					busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})

			# 確認一切正常之後，才將網頁內容填入資料表
			for data in annual_cashflow_datas:
				if data.string != None:
					if r'繼續營業單位稅前淨利（淨損）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.profit_loss_from_continuing_operations_before_tax = string_to_decimal(next_data.string)
							# print('繼續營業單位稅前淨利（淨損）:' + str(cash_flow.profit_loss_from_continuing_operations_before_tax))
					elif r'本期稅前淨利（淨損）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.profit_loss_before_tax = string_to_decimal(next_data.string)
							# print('本期稅前淨利（淨損）:' + str(cash_flow.profit_loss_before_tax))
					elif r'折舊費用' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.depreciation_expense = string_to_decimal(next_data.string)
							# print('折舊費用:' + str(cash_flow.depreciation_expense))
					elif r'攤銷費用' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.amortization_expense = string_to_decimal(next_data.string)
							# print('攤銷費用:' + str(cash_flow.amortization_expense))
					elif r'透過損益按公允價值衡量金融資產及負債之淨損失（利益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = string_to_decimal(next_data.string)
							# print('透過損益按公允價值衡量金融資產及負債之淨損失（利益）:' + str(cash_flow.net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss))
					elif r'利息費用' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.interest_expense = string_to_decimal(next_data.string)
							# print('利息費用:' + str(cash_flow.interest_expense))
					elif r'利息收入' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.interest_income = string_to_decimal(next_data.string)
							# print('利息收入:' + str(cash_flow.interest_income))
					elif r'股份基礎給付酬勞成本' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.share_based_payments = string_to_decimal(next_data.string)
							# print('股份基礎給付酬勞成本:' + str(cash_flow.share_based_payments))
					elif r'採用權益法認列之關聯企業及合資損失（利益）之份額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = string_to_decimal(next_data.string)
							# print('採用權益法認列之關聯企業及合資損失（利益）之份額:' + str(cash_flow.share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method))
					elif r'處分及報廢不動產、廠房及設備損失（利益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment = string_to_decimal(next_data.string)
							# print('處分及報廢不動產、廠房及設備損失（利益）:' + str(cash_flow.loss_gain_on_disposal_of_property_plan_and_equipment))
					elif r'處分投資損失（利益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.loss_gain_on_disposal_of_investments = string_to_decimal(next_data.string)
							# print('處分投資損失（利益）:' + str(cash_flow.loss_gain_on_disposal_of_investments))
					elif r'處分採用權益法之投資損失（利益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = string_to_decimal(next_data.string)
							# print('處分採用權益法之投資損失（利益）:' + str(cash_flow.loss_gain_on_disposal_of_investments_accounted_for_using_equity_method))
					elif r'已實現銷貨損失（利益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.realized_loss_profit_on_from_sales = string_to_decimal(next_data.string)
							# print('已實現銷貨損失（利益）:' + str(cash_flow.realized_loss_profit_on_from_sales))
					elif r'未實現外幣兌換損失（利益）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.unrealized_foreign_exchange_loss_gain = string_to_decimal(next_data.string)
							# print('未實現外幣兌換損失（利益）:' + str(cash_flow.unrealized_foreign_exchange_loss_gain))
					elif r'其他項目' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.other_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
							# print('其他項目:' + str(cash_flow.other_adjustments_to_reconcile_profit_loss))
					elif r'不影響現金流量之收益費損項目合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.total_adjustments_to_reconcile_profit_loss = string_to_decimal(next_data.string)
							# print('不影響現金流量之收益費損項目合計:' + str(cash_flow.total_adjustments_to_reconcile_profit_loss))
					elif r'持有供交易之金融資產（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_financial_assets_held_for_trading = string_to_decimal(next_data.string)
							# print('持有供交易之金融資產（增加）減少:' + str(cash_flow.decrease_increase_in_financial_assets_held_for_trading))
					elif r'避險之衍生金融資產（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging = string_to_decimal(next_data.string)
							# print('避險之衍生金融資產（增加）減少:' + str(cash_flow.decrease_increase_in_derivative_financial_assets_for_hedging))
					elif r'應收票據（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_notes_receivable = string_to_decimal(next_data.string)
							# print('應收票據（增加）減少:' + str(cash_flow.decrease_increase_in_notes_receivable))
					elif r'應收帳款（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_accounts_receivable = string_to_decimal(next_data.string)
							# print('應收帳款（增加）減少:' + str(cash_flow.decrease_increase_in_accounts_receivable))
					elif r'應收帳款－關係人（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties = string_to_decimal(next_data.string)
							# print('應收帳款－關係人（增加）減少:' + str(cash_flow.decrease_increase_in_accounts_receivable_due_from_related_parties))
					elif r'其他應收款－關係人（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_other_receivable_due_from_related_parties = string_to_decimal(next_data.string)
							# print('其他應收款－關係人（增加）減少:' + str(cash_flow.decrease_increase_in_other_receivable_due_from_related_parties))
					elif r'存貨（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_inventories = string_to_decimal(next_data.string)
							# print('存貨（增加）減少:' + str(cash_flow.decrease_increase_in_inventories))
					elif r'預付款項（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_prepayments = string_to_decimal(next_data.string)
							# print('預付款項（增加）減少:' + str(cash_flow.decrease_increase_in_prepayments))
					elif r'其他流動資產（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_other_current_assets = string_to_decimal(next_data.string)
							# print('其他流動資產（增加）減少:' + str(cash_flow.decrease_increase_in_other_current_assets))
					elif r'其他金融資產（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_other_financial_assets = string_to_decimal(next_data.string)
							# print('其他金融資產（增加）減少:' + str(cash_flow.decrease_increase_in_other_financial_assets))
					elif r'其他營業資產（增加）減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_increase_in_other_operating_assets = string_to_decimal(next_data.string)
							# print('其他營業資產（增加）減少:' + str(cash_flow.decrease_increase_in_other_operating_assets))
					elif r'與營業活動相關之資產之淨變動合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.total_changes_in_operating_assets = string_to_decimal(next_data.string)
							# print('與營業活動相關之資產之淨變動合計:' + str(cash_flow.total_changes_in_operating_assets))
					elif r'應付帳款增加（減少）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_decrease_in_accounts_payable = string_to_decimal(next_data.string)
							# print('應付帳款增加（減少）:' + str(cash_flow.increase_decrease_in_accounts_payable))
					elif r'應付帳款－關係人增加（減少）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_decrease_in_accounts_payable_to_related_parties = string_to_decimal(next_data.string)
							# print('應付帳款－關係人增加（減少）:' + str(cash_flow.increase_decrease_in_accounts_payable_to_related_parties))
					elif r'其他應付款增加（減少）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_decrease_in_other_payable = string_to_decimal(next_data.string)
							# print('其他應付款增加（減少）:' + str(cash_flow.increase_decrease_in_other_payable))
					elif r'負債準備增加（減少）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_decrease_in_provisions = string_to_decimal(next_data.string)
							# print('負債準備增加（減少）:' + str(cash_flow.increase_decrease_in_provisions))
					elif r'其他流動負債增加（減少）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_decrease_in_other_current_liabilities = string_to_decimal(next_data.string)
							# print('其他流動負債增加（減少）:' + str(cash_flow.increase_decrease_in_other_current_liabilities))
					elif r'應計退休金負債增加（減少）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_decrease_in_accrued_pension_liabilities = string_to_decimal(next_data.string)
							# print('應計退休金負債增加（減少）:' + str(cash_flow.increase_decrease_in_accrued_pension_liabilities))
					elif r'與營業活動相關之負債之淨變動合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.total_changes_in_operating_liabilities = string_to_decimal(next_data.string)
							# print('與營業活動相關之負債之淨變動合計:' + str(cash_flow.total_changes_in_operating_liabilities))
					elif r'與營業活動相關之資產及負債之淨變動合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.total_changes_in_operating_assets_and_liabilities = string_to_decimal(next_data.string)
							# print('與營業活動相關之資產及負債之淨變動合計:' + str(cash_flow.total_changes_in_operating_assets_and_liabilities))
					elif r'調整項目合計' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.total_adjustments = string_to_decimal(next_data.string)
							# print('調整項目合計:' + str(cash_flow.total_adjustments))
					elif r'營運產生之現金流入（流出）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.cash_inflow_outflow_generated_from_operations = string_to_decimal(next_data.string)
							# print('營運產生之現金流入（流出）:' + str(cash_flow.cash_inflow_outflow_generated_from_operations))
					elif r'退還（支付）之所得稅' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.income_taxes_refund_paid = string_to_decimal(next_data.string)
							# print('退還（支付）之所得稅:' + str(cash_flow.income_taxes_refund_paid))
					elif r'營業活動之淨現金流入（流出）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.net_cash_flows_from_used_in_operating_activities = string_to_decimal(next_data.string)
							# print('營業活動之淨現金流入（流出）:' + str(cash_flow.net_cash_flows_from_used_in_operating_activities))
					elif r'取得備供出售金融資產' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.acquisition_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
							# print('取得備供出售金融資產:' + str(cash_flow.acquisition_of_available_for_sale_financial_assets))
					elif r'處分備供出售金融資產' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets = string_to_decimal(next_data.string)
							# print('處分備供出售金融資產:' + str(cash_flow.proceeds_from_disposal_of_available_for_sale_financial_assets))
					elif r'持有至到期日金融資產到期還本' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets = string_to_decimal(next_data.string)
							# print('持有至到期日金融資產到期還本:' + str(cash_flow.proceeds_from_repayments_of_held_to_maturity_financial_assets))
					elif r'取得以成本衡量之金融資產' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.acquisition_of_financial_assets_at_cost = string_to_decimal(next_data.string)
							# print('取得以成本衡量之金融資產:' + str(cash_flow.acquisition_of_financial_assets_at_cost))
					elif r'處分以成本衡量之金融資產' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.proceeds_from_disposal_of_financial_assets_at_cost = string_to_decimal(next_data.string)
							# print('處分以成本衡量之金融資產:' + str(cash_flow.proceeds_from_disposal_of_financial_assets_at_cost))
					elif r'取得不動產、廠房及設備' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.acquisition_of_property_plant_and_equipment = string_to_decimal(next_data.string)
							# print('取得不動產、廠房及設備:' + str(cash_flow.acquisition_of_property_plant_and_equipment))
					elif r'處分不動產、廠房及設備' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.proceeds_from_disposal_of_property_plant_and_equipment = string_to_decimal(next_data.string)
							# print('處分不動產、廠房及設備:' + str(cash_flow.proceeds_from_disposal_of_property_plant_and_equipment))
					elif r'取得無形資產' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.acquisition_of_intangible_assets = string_to_decimal(next_data.string)
							# print('取得無形資產:' + str(cash_flow.acquisition_of_intangible_assets))
					elif r'其他非流動資產增加' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_in_other_non_current_assets = string_to_decimal(next_data.string)
							# print('其他非流動資產增加:' + str(cash_flow.increase_in_other_non_current_assets))
					elif r'投資活動之淨現金流入（流出）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.net_cash_flows_from_used_in_investing_activities = string_to_decimal(next_data.string)
							# print('投資活動之淨現金流入（流出）:' + str(cash_flow.net_cash_flows_from_used_in_investing_activities))
					elif r'短期借款增加' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_in_short_term_loans = string_to_decimal(next_data.string)
							# print('短期借款增加:' + str(cash_flow.increase_in_short_term_loans))
					elif r'短期借款減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_in_short_term_loans = string_to_decimal(next_data.string)
							# print('短期借款減少:' + str(cash_flow.decrease_in_short_term_loans))
					elif r'應付短期票券增加' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.increase_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
							# print('應付短期票券增加:' + str(cash_flow.increase_in_short_term_notes_and_bills_payable))
					elif r'應付短期票券減少' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.decrease_in_short_term_notes_and_bills_payable = string_to_decimal(next_data.string)
							# print('應付短期票券減少:' + str(cash_flow.decrease_in_short_term_notes_and_bills_payable))
					elif r'發行公司債' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.proceeds_from_issuing_bonds = string_to_decimal(next_data.string)
							# print('發行公司債:' + str(cash_flow.proceeds_from_issuing_bonds))
					elif r'償還公司債' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.repayments_of_bonds = string_to_decimal(next_data.string)
							# print('償還公司債:' + str(cash_flow.repayments_of_bonds))
					elif r'舉借長期借款' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.proceeds_from_long_term_debt = string_to_decimal(next_data.string)
							# print('舉借長期借款:' + str(cash_flow.proceeds_from_long_term_debt))
					elif r'償還長期借款' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.repayments_of_long_term_debt = string_to_decimal(next_data.string)
							# print('償還長期借款:' + str(cash_flow.repayments_of_long_term_debt))
					elif r'庫藏股票買回成本' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.payments_to_acquire_treasury_shares = string_to_decimal(next_data.string)
							# print('庫藏股票買回成本:' + str(cash_flow.payments_to_acquire_treasury_shares))
					elif r'庫藏股票處分' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.proceeds_from_sale_of_treasury_shares = string_to_decimal(next_data.string)
							# print('庫藏股票處分:' + str(cash_flow.proceeds_from_sale_of_treasury_shares))
					elif r'發放現金股利' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.cash_dividends_paid = string_to_decimal(next_data.string)
							# print('發放現金股利:' + str(cash_flow.cash_dividends_paid))
					elif r'籌資活動之淨現金流入（流出）' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.net_cash_flows_from_used_in_financing_activities = string_to_decimal(next_data.string)
							# print('籌資活動之淨現金流入（流出）:' + str(cash_flow.net_cash_flows_from_used_in_financing_activities))
					elif r'匯率變動對現金及約當現金之影響' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = string_to_decimal(next_data.string)
							# print('匯率變動對現金及約當現金之影響:' + str(cash_flow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents))
					elif r'本期現金及約當現金增加（減少）數' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.net_increase_decrease_in_cash_and_cash_equivalents = string_to_decimal(next_data.string)
							# print('本期現金及約當現金增加（減少）數:' + str(cash_flow.net_increase_decrease_in_cash_and_cash_equivalents))
					elif r'期初現金及約當現金餘額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.cash_and_cash_equivalents_at_beginning_of_period = string_to_decimal(next_data.string)
							# print('期初現金及約當現金餘額:' + str(cash_flow.cash_and_cash_equivalents_at_beginning_of_period))
					elif r'期末現金及約當現金餘額' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.cash_and_cash_equivalents_at_end_of_period = string_to_decimal(next_data.string)
							# print('期末現金及約當現金餘額:' + str(cash_flow.cash_and_cash_equivalents_at_end_of_period))
					elif r'資產負債表帳列之現金及約當現金' in data.string.encode('utf-8'):
						if data.next_sibling.next_sibling.string is not None:
							next_data = data.next_sibling.next_sibling
							cash_flow.cash_and_cash_equivalents_reported_in_the_statement_of_financial_position = string_to_decimal(next_data.string)
							# print('資產負債表帳列之現金及約當現金:' + str(cash_flow.cash_and_cash_equivalents_reported_in_the_statement_of_financial_position))
			cash_flow.free_cash_flow = 0
			if cash_flow.net_cash_flows_from_used_in_operating_activities != None:
				cash_flow.free_cash_flow = cash_flow.free_cash_flow + cash_flow.net_cash_flows_from_used_in_operating_activities
			if cash_flow.net_cash_flows_from_used_in_investing_activities != None:
				cash_flow.free_cash_flow = cash_flow.free_cash_flow + cash_flow.net_cash_flows_from_used_in_investing_activities
			# print('自由現金流量:' + str(cash_flow.free_cash_flow))

			response.close()
			# 確定有抓到期末現金及約當現金餘額的值，才將該檔股票資料寫入資料表中
			if cash_flow.cash_and_cash_equivalents_at_end_of_period is not None:
				cash_flow.save()
				print(symbol + " updated.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ") @ " + str(datetime.now()))
			else:
				print(symbol + " no data.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ")")

	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name": "現金流量表(年)"})

# 財務比率表（季）
def season_financial_ratio(request):

	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()	
	# c.execute('DELETE FROM stockfins_seasonfinancialratio')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	# # 輸入西元年(時間參數改由最外層控制)
	# yr = 2014 
	# season = [2]

	start_time = datetime.now()

	for qtr in season:
		financial_ratio = SeasonFinancialRatio()
		count = 0
		stocks = StockID.objects.all()[count:]
		countAll = stocks.count() # 計算全部需要更新的股票檔數

		for stock in stocks:
			symbol = stock.symbol
			count = count + 1
			id_filter = str(yr) + 'Q' + str(qtr) + '-' + symbol
			if qtr == 1:
				id_filter_preivous = str(yr - 1) + 'Q' + str(qtr + 3) + '-' + symbol
			else:
				id_filter_preivous = str(yr) + 'Q' + str(qtr - 1) + '-' + symbol
			has_bs_previous = False

			# 檢查本季和上一季的3大報表是否都有該檔股票的資料存在，若否，傳回錯誤訊息
			try:
				SeasonBalanceSheet.objects.get(ID=id_filter)
				SeasonIncomeStatement.objects.get(ID=id_filter)
				SeasonCashFlow.objects.get(ID=id_filter)
			except ObjectDoesNotExist:
				print(symbol + " no data.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")
				continue
			else:
				bs_Season = SeasonBalanceSheet.objects.get(ID=id_filter)
				is_Season = SeasonIncomeStatement.objects.get(ID=id_filter)
				cf_Season = SeasonCashFlow.objects.get(ID=id_filter)
				if SeasonBalanceSheet.objects.filter(ID=id_filter_preivous):
					has_bs_previous = True
					bs_Season_previous = SeasonBalanceSheet.objects.get(ID=id_filter_preivous)

				# 先宣告所有報表項目
				financial_ratio.ID = str(yr) + 'Q' + str(qtr) + '-' + symbol
				financial_ratio.symbol = symbol
				financial_ratio.year = yr
				financial_ratio.season = 'Q' + str(qtr)
				financial_ratio.date = str(yr) + 'Q' + str(qtr)
				financial_ratio.gross_profit_margin = None
				financial_ratio.operating_profit_margin = None
				financial_ratio.net_profit_margin_before_tax = None
				financial_ratio.net_profit_margin = None
				financial_ratio.earnings_per_share = None
				financial_ratio.return_on_assets = None
				financial_ratio.return_on_equity = None
				financial_ratio.current_ratio = None
				financial_ratio.quick_ratio = None
				financial_ratio.financial_debt_ratio = None
				financial_ratio.debt_ratio = None
				financial_ratio.accounts_receivable_turnover_ratio = None
				financial_ratio.inventory_turnover_ratio = None
				financial_ratio.fixed_asset_turnover_ratio = None
				financial_ratio.total_asset_turnover_ratio = None
				financial_ratio.inventory_sales_ratio = None
				financial_ratio.available_for_sale_to_equity_ratio = None
				financial_ratio.intangible_asset_to_equity_ratio = None
				financial_ratio.undepreciation_ratio = None
				financial_ratio.depreciation_to_sales_ratio = None
				financial_ratio.operating_profit_to_net_profit_before_tax_ratio = None
				financial_ratio.payout_ratio = None
				financial_ratio.tax_rate = None

				# 毛利率 = 營業毛利（毛損）淨額 / 營業收入合計（單位：％）
				if is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue != 0:
					numerator = Decimal(0)
					if is_decimal(is_Season.gross_profit_loss_from_operations_net):
						numerator = is_Season.gross_profit_loss_from_operations_net
					# 有的公司使用舊式報表，沒有營業毛利這一項，就改用繼續營業單位稅前淨利代替
					elif is_decimal(is_Season.profit_loss_from_continuing_operations_before_tax):
						numerator = is_Season.profit_loss_from_continuing_operations_before_tax
					financial_ratio.gross_profit_margin = numerator / is_Season.total_operating_revenue * 100
				elif is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue == 0:
					financial_ratio.gross_profit_margin = 0
				# 營益率 = 營業利益（損失） / 營業收入合計（單位：％）
				if is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue != 0:
					numerator = Decimal(0)
					if is_decimal(is_Season.net_operating_income_loss):
						numerator = is_Season.net_operating_income_loss
					# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
					elif is_decimal(is_Season.profit_loss_from_continuing_operations_before_tax):
						numerator = is_Season.profit_loss_from_continuing_operations_before_tax
					financial_ratio.operating_profit_margin = numerator / is_Season.total_operating_revenue * 100
				elif is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue == 0:
					financial_ratio.operating_profit_margin = 0
				# 稅前淨利率 = 稅前淨利（淨損） / 營業收入合計（單位：％）
				if is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue != 0:
					numerator = Decimal(0)
					if is_decimal(is_Season.profit_loss_from_continuing_operations_before_tax):
						numerator = is_Season.profit_loss_from_continuing_operations_before_tax
					financial_ratio.net_profit_margin_before_tax = numerator / is_Season.total_operating_revenue * 100
				elif is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue == 0:
					financial_ratio.net_profit_margin_before_tax = 0
				# 稅後淨利率 = 本期淨利（淨損） / 營業收入合計（單位：％）
				if is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue != 0:
					numerator = Decimal(0)
					if is_decimal(is_Season.profit_loss):
						numerator = is_Season.profit_loss
					financial_ratio.net_profit_margin = numerator / is_Season.total_operating_revenue * 100
				elif is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue == 0:
					financial_ratio.net_profit_margin = 0
				# 每股盈餘(EPS) = 基本每股盈餘（單位：元/股）
				if is_decimal(is_Season.total_basic_earnings_per_share):
					financial_ratio.earnings_per_share = is_Season.total_basic_earnings_per_share
				#?? 總資產報酬率(ROA) = 本期淨利（淨損） / 期初期末平均之資產總額（單位：％）
				if is_decimal(is_Season.profit_loss):
					denumerator = Decimal(1)
					numerator = Decimal(0)
					numerator = is_Season.profit_loss
					if is_decimal(bs_Season.total_assets):
						denumerator = denumerator + bs_Season.total_assets
					if has_bs_previous:
						if is_decimal(bs_Season_previous.total_assets):
							denumerator = denumerator + bs_Season_previous.total_assets
						denumerator = denumerator / 2
					financial_ratio.return_on_assets = numerator / denumerator * 100
				else:
					financial_ratio.return_on_assets = 0
				# 股東權益報酬率(ROE) = 本期淨利（淨損） / 期初期末平均之權益總額（單位：％）
				if is_decimal(is_Season.profit_loss):
					denumerator = Decimal(1)
					numerator = Decimal(0)
					numerator = is_Season.profit_loss
					if is_decimal(bs_Season.total_equity):
						denumerator = denumerator + bs_Season.total_equity
					if has_bs_previous:
						if is_decimal(bs_Season_previous.total_equity):
							denumerator = denumerator + bs_Season_previous.total_equity
						denumerator = denumerator / 2
					financial_ratio.return_on_equity = numerator / denumerator * 100
				else:
					financial_ratio.return_on_equity = 0
				# 流動比率 = 流動資產合計 / 流動負債合計
				if is_decimal(bs_Season.total_current_liabilities) and bs_Season.total_current_liabilities != 0:
					numerator = Decimal(0)
					if is_decimal(bs_Season.total_current_assets):
						numerator = bs_Season.total_current_assets
					financial_ratio.current_ratio = numerator / bs_Season.total_current_liabilities * 100
				# 速動比率 = 速動資產合計 / 流動負債合計（速動資產 = 流動資產 - 存貨 - 預付款項 - 其他流動資產）
				if is_decimal(bs_Season.total_current_liabilities) and bs_Season.total_current_liabilities != 0:
					numerator = Decimal(0)
					if is_decimal(bs_Season.total_current_assets):
						numerator = numerator + bs_Season.total_current_assets
					if is_decimal(bs_Season.total_inventories):
						numerator = numerator - bs_Season.total_inventories
					if is_decimal(bs_Season.total_prepayments):
						numerator = numerator - bs_Season.total_prepayments
					if is_decimal(bs_Season.total_other_current_assets):
						numerator = numerator - bs_Season.total_other_current_assets
					financial_ratio.quick_ratio = numerator / bs_Season.total_current_liabilities * 100
				#?? 金融負債比率 = 金融負債總額 / 資產總額（金融負債 = 短期借款 + 應付短期票券 + 應付公司債 + 長期借款，要付息的，單位：％）
				if is_decimal(bs_Season.total_assets) and bs_Season.total_assets != 0:
					numerator = Decimal(0)
					if is_decimal(bs_Season.total_short_term_borrowings):
						numerator = numerator + bs_Season.total_short_term_borrowings
					if is_decimal(bs_Season.total_short_term_notes_and_bills_payable):
						numerator = numerator + bs_Season.total_short_term_notes_and_bills_payable
					if is_decimal(bs_Season.total_bonds_payable):
						numerator = numerator + bs_Season.total_bonds_payable
					if is_decimal(bs_Season.total_long_borrowings):
						numerator = numerator + bs_Season.total_long_borrowings
					financial_ratio.financial_debt_ratio = numerator / bs_Season.total_assets * 100
				# 負債比率 = 負債總額 / 資產總額（單位：％）
				if is_decimal(bs_Season.total_assets) and bs_Season.total_assets != 0:
					numerator = Decimal(0)
					if is_decimal(bs_Season.total_liabilities):
						numerator = bs_Season.total_liabilities
					financial_ratio.debt_ratio = numerator / bs_Season.total_assets * 100
				# 應收帳款週轉率 = 營業收入合計 / 期初期末平均之應收票據淨額+應收帳款淨額+應收帳款－關係人淨額（單位：次／季）
				if is_decimal(is_Season.total_operating_revenue):
					denumerator = Decimal(1)
					numerator = Decimal(0)
					numerator = is_Season.total_operating_revenue
					if is_decimal(bs_Season.notes_receivable_net):
						denumerator = denumerator + bs_Season.notes_receivable_net
					if is_decimal(bs_Season.accounts_receivable_net):
						denumerator = denumerator + bs_Season.accounts_receivable_net
					if is_decimal(bs_Season.accounts_receivable_due_from_related_parties_net):
						denumerator = denumerator + bs_Season.accounts_receivable_due_from_related_parties_net
					if has_bs_previous:
						if is_decimal(bs_Season_previous.notes_receivable_net):
							denumerator = denumerator + bs_Season_previous.notes_receivable_net
						if is_decimal(bs_Season_previous.accounts_receivable_net):
							denumerator = denumerator + bs_Season_previous.accounts_receivable_net
						if is_decimal(bs_Season_previous.accounts_receivable_due_from_related_parties_net):
							denumerator = denumerator + bs_Season_previous.accounts_receivable_due_from_related_parties_net
						denumerator = denumerator / 2
					financial_ratio.accounts_receivable_turnover_ratio = numerator / denumerator * 4
				else:
					financial_ratio.accounts_receivable_turnover_ratio = 0
				# 存貨週轉率 = 營業成本合計 / 期初期末平均之存貨（單位：次／季）
				if is_decimal(is_Season.total_operating_costs):
					denumerator = Decimal(1)
					numerator = Decimal(0)
					numerator = is_Season.total_operating_costs
					if is_decimal(bs_Season.total_inventories):
						denumerator = denumerator + bs_Season.total_inventories
					if has_bs_previous:
						if is_decimal(bs_Season_previous.total_inventories):
							denumerator = denumerator + bs_Season_previous.total_inventories
						denumerator = denumerator / 2
					financial_ratio.inventory_turnover_ratio = numerator / denumerator * 4
				else:
					financial_ratio.inventory_turnover_ratio = 0
				# 固定資產週轉率 = 營業收入合計 / 期初期末平均之不動產、廠房及設備（單位：次／季）
				if is_decimal(is_Season.total_operating_revenue):
					denumerator = Decimal(1)
					numerator = Decimal(0)
					numerator = is_Season.total_operating_revenue
					if is_decimal(bs_Season.total_property_plant_and_equipment):
						denumerator = denumerator + bs_Season.total_property_plant_and_equipment
					if has_bs_previous:
						if is_decimal(bs_Season_previous.total_property_plant_and_equipment):
							denumerator = denumerator + bs_Season_previous.total_property_plant_and_equipment
						denumerator = denumerator / 2
					financial_ratio.fixed_asset_turnover_ratio = numerator / denumerator * 4
				else:
					financial_ratio.fixed_asset_turnover_ratio = 0
				# 總資產週轉率 = 營業收入合計 / 期初期末平均之資產總額（單位：次／季）
				if is_decimal(is_Season.total_operating_revenue):
					denumerator = Decimal(1)
					numerator = Decimal(0)
					numerator = is_Season.total_operating_revenue
					if is_decimal(bs_Season.total_assets):
						denumerator = denumerator + bs_Season.total_assets
					if has_bs_previous:
						if is_decimal(bs_Season_previous.total_assets):
							denumerator = denumerator + bs_Season_previous.total_assets
						denumerator = denumerator / 2
					financial_ratio.total_asset_turnover_ratio = numerator / denumerator * 4
				else:
					financial_ratio.total_asset_turnover_ratio = 0
				# 存貨營收比 = 存貨 / 營業收入合計（評估存貨要多少季可以消化完畢，單位：季）
				if is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue != 0:
					numerator = Decimal(0)
					if is_decimal(bs_Season.total_inventories):
						numerator = bs_Season.total_inventories
					financial_ratio.inventory_sales_ratio = numerator / is_Season.total_operating_revenue
				elif is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue == 0:
					financial_ratio.inventory_sales_ratio = 999
				# 備供出售比率 = 備供出售金融資產－非流動淨額 / 權益總額（單位：％）
				if is_decimal(bs_Season.total_equity) and bs_Season.total_equity != 0:
					numerator = Decimal(0)
					if is_decimal(bs_Season.non_current_available_for_sale_financial_assets_net):
						numerator = bs_Season.non_current_available_for_sale_financial_assets_net
					financial_ratio.available_for_sale_to_equity_ratio = numerator / bs_Season.total_equity * 100
				# 無形資產比率 = 無形資產 / 權益總額（單位：％）
				if is_decimal(bs_Season.total_equity) and bs_Season.total_equity != 0:
					numerator = Decimal(0)
					if is_decimal(bs_Season.total_intangible_assets):
						numerator = bs_Season.total_intangible_assets
					financial_ratio.intangible_asset_to_equity_ratio = numerator / bs_Season.total_equity * 100
				#未折舊比率（新式財報中已經沒有累積折舊項目，因此無法計算）

				#?? 折舊負擔比率 = 折舊費用 / 營業收入合計（評估營收必須拿多少來攤提折舊，單位：％）
				if is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue != 0:
					numerator = Decimal(0)
					if is_decimal(cf_Season.depreciation_expense):
						numerator = cf_Season.depreciation_expense
					financial_ratio.depreciation_to_sales_ratio = numerator / is_Season.total_operating_revenue * 100
				elif is_decimal(is_Season.total_operating_revenue) and is_Season.total_operating_revenue == 0:
					financial_ratio.depreciation_to_sales_ratio = 999
				# 營業利益佔稅前淨利比率 = 營業利益（損失） / 稅前淨利（淨損）（單位：％）
				if is_decimal(is_Season.profit_loss_from_continuing_operations_before_tax) and is_Season.profit_loss_from_continuing_operations_before_tax != 0:
					numerator = Decimal(0)
					if is_decimal(is_Season.net_operating_income_loss):
						numerator = numerator + is_Season.net_operating_income_loss
					# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
					elif is_decimal(is_Season.profit_loss_from_continuing_operations_before_tax):
						numerator = numerator + is_Season.profit_loss_from_continuing_operations_before_tax
					financial_ratio.operating_profit_to_net_profit_before_tax_ratio = numerator / is_Season.profit_loss_from_continuing_operations_before_tax * 100
				# 現金股息配發率(季資料忽略此項目)

				# 營業稅率 = 所得稅費用（利益）合計 / 稅前淨利（淨損）（單位：％）
				if is_decimal(is_Season.profit_loss_from_continuing_operations_before_tax) and is_Season.profit_loss_from_continuing_operations_before_tax != 0:
					numerator = Decimal(0)
					if is_decimal(is_Season.total_tax_expense_income):
						numerator = numerator + is_Season.total_tax_expense_income
						if is_Season.profit_loss_from_continuing_operations_before_tax < 0:
							financial_ratio.tax_rate = numerator / (-is_Season.profit_loss_from_continuing_operations_before_tax) * 100
						else:
							financial_ratio.tax_rate = numerator / is_Season.profit_loss_from_continuing_operations_before_tax * 100
					else:
						financial_ratio.tax_rate = numerator / is_Season.profit_loss_from_continuing_operations_before_tax * 100

				if financial_ratio.earnings_per_share is not None:
					financial_ratio.save()
					print(symbol + " calculated.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ") @ " + str(datetime.now()))
				else:
					print(symbol + " doesn't save.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + "-Q"  + str(qtr) + ")")

	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name": "財務比率表（季）"})

# 財務比率表（年）
def annual_financial_ratio(request):

	# # 如果要重建資料表的話，請將以下這段文字的註解拿掉
	# conn = sqlite3.connect(os.path.join(BASE_DIR, 'pickstock.db'))
	# conn.text_factory = str
	# c = conn.cursor()	
	# c.execute('DELETE FROM stockfins_annualfinancialratio')
	# conn.commit()
	# c.close()
	# conn.close()
	# print('old table has been cleaned.')

	# # 輸入西元年(時間參數改由最外層控制)
	# yr = 2014

	start_time = datetime.now()

	financial_ratio = AnnualFinancialRatio()
	count = 0
	stocks = StockID.objects.all()[count:]
	countAll = stocks.count() # 計算全部需要更新的股票檔數

	for stock in stocks:
		symbol = stock.symbol
		count = count + 1
		id_filter = str(yr) + '-' + symbol
		id_filter_bs = str(yr) + 'Q4-' + symbol
		id_filter_preivous = str(yr - 1) + '-' + symbol
		id_filter_bs_preivous = str(yr - 1) + 'Q4-' + symbol
		has_bs_previous = False

		# 檢查本年和上一年的3大報表是否都有該檔股票的資料存在，若否，傳回錯誤訊息
		try:
			SeasonBalanceSheet.objects.get(ID=id_filter_bs)
			AnnualIncomeStatement.objects.get(ID=id_filter)
			AnnualCashFlow.objects.get(ID=id_filter)
			# EarningsPayout.objects.get(ID=id_filter)
		except ObjectDoesNotExist:
			print(symbol + " no data.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ")")
			continue
		else:
			bs_Annual = SeasonBalanceSheet.objects.get(ID=id_filter_bs)
			is_Annual = AnnualIncomeStatement.objects.get(ID=id_filter)
			cf_Annual = AnnualCashFlow.objects.get(ID=id_filter)
			# 改放在下方計算配息率時才做判斷
			# ep_Annual = EarningsPayout.objects.get(ID=id_filter)
			if SeasonBalanceSheet.objects.filter(ID=id_filter_bs_preivous):
				has_bs_previous = True
				bs_Annual_previous = SeasonBalanceSheet.objects.get(ID=id_filter_bs_preivous)

			# 先宣告所有報表項目
			financial_ratio.ID = str(yr) + '-' + symbol
			financial_ratio.symbol = symbol
			financial_ratio.year = yr
			financial_ratio.gross_profit_margin = None
			financial_ratio.operating_profit_margin = None
			financial_ratio.net_profit_margin_before_tax = None
			financial_ratio.net_profit_margin = None
			financial_ratio.earnings_per_share = None
			financial_ratio.return_on_assets = None
			financial_ratio.return_on_equity = None
			financial_ratio.current_ratio = None
			financial_ratio.quick_ratio = None
			financial_ratio.financial_debt_ratio = None
			financial_ratio.debt_ratio = None
			financial_ratio.accounts_receivable_turnover_ratio = None
			financial_ratio.inventory_turnover_ratio = None
			financial_ratio.fixed_asset_turnover_ratio = None
			financial_ratio.total_asset_turnover_ratio = None
			financial_ratio.inventory_sales_ratio = None
			financial_ratio.available_for_sale_to_equity_ratio = None
			financial_ratio.intangible_asset_to_equity_ratio = None
			financial_ratio.undepreciation_ratio = None
			financial_ratio.depreciation_to_sales_ratio = None
			financial_ratio.operating_profit_to_net_profit_before_tax_ratio = None
			financial_ratio.payout_ratio = None
			financial_ratio.tax_rate = None

			# 毛利率 = 營業毛利（毛損）淨額 / 營業收入合計（單位：％）
			if is_decimal(is_Annual.total_operating_revenue) and is_Annual.total_operating_revenue != 0:
				numerator = Decimal(0)
				if is_decimal(is_Annual.gross_profit_loss_from_operations_net):
					numerator = is_Annual.gross_profit_loss_from_operations_net
				# 有的公司使用舊式報表，沒有營業毛利這一項，就改用繼續營業單位稅前淨利代替
				elif is_decimal(is_Annual.profit_loss_from_continuing_operations_before_tax):
					numerator = is_Annual.profit_loss_from_continuing_operations_before_tax
				financial_ratio.gross_profit_margin = numerator / is_Annual.total_operating_revenue * 100
			# 營益率 = 營業利益（損失） / 營業收入合計（單位：％）
			if is_decimal(is_Annual.total_operating_revenue) and is_Annual.total_operating_revenue != 0:
				numerator = Decimal(0)
				if is_decimal(is_Annual.net_operating_income_loss):
					numerator = is_Annual.net_operating_income_loss
				# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
				elif is_decimal(is_Annual.profit_loss_from_continuing_operations_before_tax):
					numerator = is_Annual.profit_loss_from_continuing_operations_before_tax
				financial_ratio.operating_profit_margin = numerator / is_Annual.total_operating_revenue * 100
			# 稅前淨利率 = 稅前淨利（淨損） / 營業收入合計（單位：％）
			if is_decimal(is_Annual.total_operating_revenue) and is_Annual.total_operating_revenue != 0:
				numerator = Decimal(0)
				if is_decimal(is_Annual.profit_loss_from_continuing_operations_before_tax):
					numerator = is_Annual.profit_loss_from_continuing_operations_before_tax
				financial_ratio.net_profit_margin_before_tax = numerator / is_Annual.total_operating_revenue * 100
			# 稅後淨利率 = 本期淨利（淨損） / 營業收入合計（單位：％）
			if is_decimal(is_Annual.total_operating_revenue) and is_Annual.total_operating_revenue != 0:
				numerator = Decimal(0)
				if is_decimal(is_Annual.profit_loss):
					numerator = is_Annual.profit_loss
				financial_ratio.net_profit_margin = numerator / is_Annual.total_operating_revenue * 100
			# 每股盈餘(EPS) = 基本每股盈餘（單位：元/股）
			if is_decimal(is_Annual.total_basic_earnings_per_share):
				financial_ratio.earnings_per_share = is_Annual.total_basic_earnings_per_share
			#?? 總資產報酬率(ROA) = 本期淨利（淨損） / 期初期末平均之資產總額（單位：％）
			if is_decimal(is_Annual.profit_loss):
				denumerator = Decimal(1)
				numerator = Decimal(0)
				numerator = is_Annual.profit_loss
				if is_decimal(bs_Annual.total_assets):
					denumerator = denumerator + bs_Annual.total_assets
				if has_bs_previous:
					if is_decimal(bs_Annual_previous.total_assets):
						denumerator = denumerator + bs_Annual_previous.total_assets
					denumerator = denumerator / 2
				financial_ratio.return_on_assets = numerator / denumerator * 100
			else:
				financial_ratio.return_on_assets = 0
			# 股東權益報酬率(ROE) = 本期淨利（淨損） / 期初期末平均之權益總額（單位：％）
			if is_decimal(is_Annual.profit_loss):
				denumerator = Decimal(1)
				numerator = Decimal(0)
				numerator = is_Annual.profit_loss
				if is_decimal(bs_Annual.total_equity):
					denumerator = denumerator + bs_Annual.total_equity
				if has_bs_previous:
					if is_decimal(bs_Annual_previous.total_equity):
						denumerator = denumerator + bs_Annual_previous.total_equity
					denumerator = denumerator / 2
				financial_ratio.return_on_equity = numerator / denumerator * 100
			else:
				financial_ratio.return_on_equity = 0
			# 流動比率 = 流動資產合計 / 流動負債合計
			if is_decimal(bs_Annual.total_current_liabilities) and bs_Annual.total_current_liabilities != 0:
				numerator = Decimal(0)
				if is_decimal(bs_Annual.total_current_assets):
					numerator = bs_Annual.total_current_assets
				financial_ratio.current_ratio = numerator / bs_Annual.total_current_liabilities * 100
			# 速動比率 = 速動資產合計 / 流動負債合計（速動資產 = 流動資產 - 存貨 - 預付款項 - 其他流動資產）
			if is_decimal(bs_Annual.total_current_liabilities) and bs_Annual.total_current_liabilities != 0:
				numerator = Decimal(0)
				if is_decimal(bs_Annual.total_current_assets):
					numerator = numerator + bs_Annual.total_current_assets
				if is_decimal(bs_Annual.total_inventories):
					numerator = numerator - bs_Annual.total_inventories
				if is_decimal(bs_Annual.total_prepayments):
					numerator = numerator - bs_Annual.total_prepayments
				if is_decimal(bs_Annual.total_other_current_assets):
					numerator = numerator - bs_Annual.total_other_current_assets
				financial_ratio.quick_ratio = numerator / bs_Annual.total_current_liabilities * 100
			#?? 金融負債比率 = 金融負債總額 / 資產總額（金融負債 = 短期借款 + 應付短期票券 + 應付公司債 + 長期借款，要付息的，單位：％）
			if is_decimal(bs_Annual.total_assets) and bs_Annual.total_assets != 0:
				numerator = Decimal(0)
				if is_decimal(bs_Annual.total_short_term_borrowings):
					numerator = numerator + bs_Annual.total_short_term_borrowings
				if is_decimal(bs_Annual.total_short_term_notes_and_bills_payable):
					numerator = numerator + bs_Annual.total_short_term_notes_and_bills_payable
				if is_decimal(bs_Annual.total_bonds_payable):
					numerator = numerator + bs_Annual.total_bonds_payable
				if is_decimal(bs_Annual.total_long_borrowings):
					numerator = numerator + bs_Annual.total_long_borrowings
				financial_ratio.financial_debt_ratio = numerator / bs_Annual.total_assets * 100
			# 負債比率 = 負債總額 / 資產總額（單位：％）
			if is_decimal(bs_Annual.total_assets) and bs_Annual.total_assets != 0:
				numerator = Decimal(0)
				if is_decimal(bs_Annual.total_liabilities):
					numerator = bs_Annual.total_liabilities
				financial_ratio.debt_ratio = numerator / bs_Annual.total_assets * 100
			# 應收帳款週轉率 = 營業收入合計 / 期初期末平均之應收票據淨額+應收帳款淨額+應收帳款－關係人淨額（單位：次／季）
			if is_decimal(is_Annual.total_operating_revenue):
				denumerator = Decimal(1)
				numerator = Decimal(0)
				numerator = is_Annual.total_operating_revenue
				if is_decimal(bs_Annual.notes_receivable_net):
					denumerator = denumerator + bs_Annual.notes_receivable_net
				if is_decimal(bs_Annual.accounts_receivable_net):
					denumerator = denumerator + bs_Annual.accounts_receivable_net
				if is_decimal(bs_Annual.accounts_receivable_due_from_related_parties_net):
					denumerator = denumerator + bs_Annual.accounts_receivable_due_from_related_parties_net
				if has_bs_previous:
					if is_decimal(bs_Annual_previous.notes_receivable_net):
						denumerator = denumerator + bs_Annual_previous.notes_receivable_net
					if is_decimal(bs_Annual_previous.accounts_receivable_net):
						denumerator = denumerator + bs_Annual_previous.accounts_receivable_net
					if is_decimal(bs_Annual_previous.accounts_receivable_due_from_related_parties_net):
						denumerator = denumerator + bs_Annual_previous.accounts_receivable_due_from_related_parties_net
					denumerator = denumerator / 2
				financial_ratio.accounts_receivable_turnover_ratio = numerator / denumerator
			else:
				financial_ratio.accounts_receivable_turnover_ratio = 0
			# 存貨週轉率 = 營業成本合計 / 期初期末平均之存貨（單位：次／季）
			if is_decimal(is_Annual.total_operating_costs):
				denumerator = Decimal(1)
				numerator = Decimal(0)
				numerator = is_Annual.total_operating_costs
				if is_decimal(bs_Annual.total_inventories):
					denumerator = denumerator + bs_Annual.total_inventories
				if has_bs_previous:
					if is_decimal(bs_Annual_previous.total_inventories):
						denumerator = denumerator + bs_Annual_previous.total_inventories
					denumerator = denumerator / 2
				financial_ratio.inventory_turnover_ratio = numerator / denumerator
			else:
				financial_ratio.inventory_turnover_ratio = 0
			# 固定資產週轉率 = 營業收入合計 / 期初期末平均之不動產、廠房及設備（單位：次／季）
			if is_decimal(is_Annual.total_operating_revenue):
				denumerator = Decimal(1)
				numerator = Decimal(0)
				numerator = is_Annual.total_operating_revenue
				if is_decimal(bs_Annual.total_property_plant_and_equipment):
					denumerator = denumerator + bs_Annual.total_property_plant_and_equipment
				if has_bs_previous:
					if is_decimal(bs_Annual_previous.total_property_plant_and_equipment):
						denumerator = denumerator + bs_Annual_previous.total_property_plant_and_equipment
					denumerator = denumerator / 2
				financial_ratio.fixed_asset_turnover_ratio = numerator / denumerator
			else:
				financial_ratio.fixed_asset_turnover_ratio = 0
			# 總資產週轉率 = 營業收入合計 / 期初期末平均之資產總額（單位：次／季）
			if is_decimal(is_Annual.total_operating_revenue):
				denumerator = Decimal(1)
				numerator = Decimal(0)
				numerator = is_Annual.total_operating_revenue
				if is_decimal(bs_Annual.total_assets):
					denumerator = denumerator + bs_Annual.total_assets
				if has_bs_previous:
					if is_decimal(bs_Annual_previous.total_assets):
						denumerator = denumerator + bs_Annual_previous.total_assets
					denumerator = denumerator / 2
				financial_ratio.total_asset_turnover_ratio = numerator / denumerator
			else:
				financial_ratio.total_asset_turnover_ratio = 0
			# 存貨營收比 = 存貨 / 營業收入合計（評估存貨要多少季可以消化完畢，單位：季）
			if is_decimal(is_Annual.total_operating_revenue) and is_Annual.total_operating_revenue != 0:
				numerator = Decimal(0)
				if is_decimal(bs_Annual.total_inventories):
					numerator = bs_Annual.total_inventories
				financial_ratio.inventory_sales_ratio = numerator / is_Annual.total_operating_revenue
			# 備供出售比率 = 備供出售金融資產－非流動淨額 / 權益總額（單位：％）
			if is_decimal(bs_Annual.total_equity) and bs_Annual.total_equity != 0:
				numerator = Decimal(0)
				if is_decimal(bs_Annual.non_current_available_for_sale_financial_assets_net):
					numerator = bs_Annual.non_current_available_for_sale_financial_assets_net
				financial_ratio.available_for_sale_to_equity_ratio = numerator / bs_Annual.total_equity * 100
			# 無形資產比率 = 無形資產 / 權益總額（單位：％）
			if is_decimal(bs_Annual.total_equity) and bs_Annual.total_equity != 0:
				numerator = Decimal(0)
				if is_decimal(bs_Annual.total_intangible_assets):
					numerator = bs_Annual.total_intangible_assets
				financial_ratio.intangible_asset_to_equity_ratio = numerator / bs_Annual.total_equity * 100
			#?? 未折舊比率（新式財報中已經沒有累積折舊項目，因此無法計算）

			#?? 折舊負擔比率 = 折舊費用 / 營業收入合計（評估營收必須拿多少來攤提折舊，單位：％）
			if is_decimal(is_Annual.total_operating_revenue) and is_Annual.total_operating_revenue != 0:
				numerator = Decimal(0)
				if is_decimal(cf_Annual.depreciation_expense):
					numerator = cf_Annual.depreciation_expense
				financial_ratio.depreciation_to_sales_ratio = numerator / is_Annual.total_operating_revenue * 100
			# 營業利益佔稅前淨利比率 = 營業利益（損失） / 稅前淨利（淨損）（單位：％）
			if is_decimal(is_Annual.profit_loss_from_continuing_operations_before_tax) and is_Annual.profit_loss_from_continuing_operations_before_tax != 0:
				numerator = Decimal(0)
				if is_decimal(is_Annual.net_operating_income_loss):
					numerator = numerator + is_Annual.net_operating_income_loss
				# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
				elif is_decimal(is_Annual.profit_loss_from_continuing_operations_before_tax):
					numerator = numerator + is_Annual.profit_loss_from_continuing_operations_before_tax
				financial_ratio.operating_profit_to_net_profit_before_tax_ratio = numerator / is_Annual.profit_loss_from_continuing_operations_before_tax * 100
			# 現金股息配發率 = 現金股利合計 / 每股盈餘(EPS)（單位：％）
			if is_decimal(is_Annual.total_basic_earnings_per_share) and is_Annual.total_basic_earnings_per_share != 0:
				numerator = Decimal(0)
				if EarningsPayout.objects.filter(ID=id_filter):
					ep_Annual = EarningsPayout.objects.get(ID=id_filter)
					if is_decimal(ep_Annual.cash_dividends_all):
						numerator = ep_Annual.cash_dividends_all
				financial_ratio.payout_ratio = numerator / is_Annual.total_basic_earnings_per_share * 100
			elif is_decimal(is_Annual.total_basic_earnings_per_share) and is_Annual.total_basic_earnings_per_share == 0:
				financial_ratio.payout_ratio = 0
			# 營業稅率 = 所得稅費用（利益）合計 / 稅前淨利（淨損）（單位：％）
			if is_decimal(is_Annual.profit_loss_from_continuing_operations_before_tax) and is_Annual.profit_loss_from_continuing_operations_before_tax != 0:
				numerator = Decimal(0)
				if is_decimal(is_Annual.total_tax_expense_income):
					numerator = numerator + is_Annual.total_tax_expense_income
					if is_Annual.profit_loss_from_continuing_operations_before_tax < 0:
						financial_ratio.tax_rate = numerator / (-is_Annual.profit_loss_from_continuing_operations_before_tax) * 100
					else:
						financial_ratio.tax_rate = numerator / is_Annual.profit_loss_from_continuing_operations_before_tax * 100
				else:
					financial_ratio.tax_rate = numerator / is_Annual.profit_loss_from_continuing_operations_before_tax * 100

			if financial_ratio.earnings_per_share is not None:
				financial_ratio.save()
				print(symbol + " calculated.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ") @ " + str(datetime.now()))
			else:
				print(symbol + " doesn't save.(" + str(count) + "/" + str(countAll) + ", " + str(yr) + ")")

	end_time = datetime.now()
	spent_time = end_time - start_time
	print(u"本次更新花費: " + str(spent_time.seconds) + u" 秒")

	return render_to_response('msg_updateOK.html', {"table_name": "財務比率表（年）"})