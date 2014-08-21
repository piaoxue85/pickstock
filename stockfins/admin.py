#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from stockfins.models import SeasonBalanceSheet, SeasonIncomeStatement, AnnualIncomeStatement, SeasonCashFlow, AnnualCashFlow
from stockfins.models import SeasonFinancialRatio, AnnualFinancialRatio, EarningsPayout

# 盈餘分配表(季)
class EarningsPayoutAdmin(admin.ModelAdmin):
	list_display = ('ID', 'year', 'symbol', 'shareholder_meeting_date', 'net_profit_after_tax',
					 'distributable_net_profit', 'cash_dividends_all','stock_dividends_all',
					 'payable_to_directors_and_supervisors', 'employee_bonus_all',
					 "modified_date")
	list_filter = ('year', 'symbol')
	search_fields = ('symbol', 'year')

admin.site.register(EarningsPayout, EarningsPayoutAdmin)

# 資產負債表(季)
class SeasonBalanceSheetAdmin(admin.ModelAdmin):
	list_display = ('ID', 'date', 'symbol', 'total_current_assets', 'total_non_current_assets',
					 'total_assets', 'total_current_liabilities','total_non_current_liabilities', 'total_liabilities',
					 'ordinary_share', 'total_capital_surplus', 'total_retained_earnings', 'total_equity_attributable_to_owners_of_parent',
					 "modified_date")
	list_filter = ('date', 'symbol')
	search_fields = ('symbol', 'date', 'year')

admin.site.register(SeasonBalanceSheet, SeasonBalanceSheetAdmin)

# 綜合損益表(季)
class SeasonIncomeStatementAdmin(admin.ModelAdmin):
	list_display = ('ID', 'date', 'symbol', 'total_operating_revenue', 'gross_profit_loss_from_operations',
					 'net_operating_income_loss', 'profit_loss','total_comprehensive_income',
					 'total_basic_earnings_per_share', "modified_date")
	list_filter = ('date', 'symbol')
	search_fields = ('symbol', 'date', 'year')

admin.site.register(SeasonIncomeStatement, SeasonIncomeStatementAdmin)

# 綜合損益表(年)
class AnnualIncomeStatementAdmin(admin.ModelAdmin):
	list_display = ('ID', 'year', 'symbol', 'total_operating_revenue', 'gross_profit_loss_from_operations',
					 'net_operating_income_loss', 'profit_loss','total_comprehensive_income',
					 'total_basic_earnings_per_share', "modified_date")
	list_filter = ('year', 'symbol')
	search_fields = ('symbol', 'year')

admin.site.register(AnnualIncomeStatement, AnnualIncomeStatementAdmin)

# 現金流量表(季)
class SeasonCashFlowAdmin(admin.ModelAdmin):
	list_display = ('ID', 'date', 'symbol', 'profit_loss_before_tax', 'net_cash_flows_from_used_in_operating_activities',
					 'net_cash_flows_from_used_in_investing_activities', 'net_cash_flows_from_used_in_financing_activities',
					 'effect_of_exchange_rate_changes_on_cash_and_cash_equivalents', 'net_increase_decrease_in_cash_and_cash_equivalents',
					 'cash_and_cash_equivalents_at_end_of_period', 'free_cash_flow', "modified_date")
	list_filter = ('date', 'symbol')
	search_fields = ('symbol', 'date', 'year')

admin.site.register(SeasonCashFlow, SeasonCashFlowAdmin)

# 現金流量表(年)
class AnnualCashFlowAdmin(admin.ModelAdmin):
	list_display = ('ID', 'year', 'symbol', 'profit_loss_before_tax', 'net_cash_flows_from_used_in_operating_activities',
					 'net_cash_flows_from_used_in_investing_activities', 'net_cash_flows_from_used_in_financing_activities',
					 'effect_of_exchange_rate_changes_on_cash_and_cash_equivalents', 'net_increase_decrease_in_cash_and_cash_equivalents',
					 'cash_and_cash_equivalents_at_end_of_period', 'free_cash_flow', "modified_date")
	list_filter = ('year', 'symbol')
	search_fields = ('symbol', 'year')

admin.site.register(AnnualCashFlow, AnnualCashFlowAdmin)

# 財務比率表(季)
class SeasonFinancialRatioAdmin(admin.ModelAdmin):
	list_display = ('ID', 'date', 'symbol',
					'gross_profit_margin', 'operating_profit_margin', 'net_profit_margin', 'earnings_per_share',
					'current_ratio', 'quick_ratio', 'financial_debt_ratio', 'debt_ratio',
					'inventory_turnover_ratio', 'fixed_asset_turnover_ratio',
					'inventory_sales_ratio', 'depreciation_to_sales_ratio', 'payout_ratio', 'tax_rate',
					"modified_date")
	list_filter = ('date', 'symbol')
	search_fields = ('symbol', 'date', 'year')

admin.site.register(SeasonFinancialRatio, SeasonFinancialRatioAdmin)

# 財務比率表(年)
class AnnualFinancialRatioAdmin(admin.ModelAdmin):
	list_display = ('ID', 'year', 'symbol',
					'gross_profit_margin', 'operating_profit_margin', 'net_profit_margin', 'earnings_per_share',
					'current_ratio', 'quick_ratio', 'financial_debt_ratio', 'debt_ratio',
					'inventory_turnover_ratio', 'fixed_asset_turnover_ratio',
					'inventory_sales_ratio', 'depreciation_to_sales_ratio', 'payout_ratio', 'tax_rate',
					"modified_date")
	list_filter = ('year', 'symbol')
	search_fields = ('symbol', 'year')

admin.site.register(AnnualFinancialRatio, AnnualFinancialRatioAdmin)