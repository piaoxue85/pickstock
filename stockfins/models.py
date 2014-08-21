#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# 盈餘分配表(年)
class EarningsPayout(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    symbol = models.CharField(max_length=20, db_index=True)
    year = models.IntegerField(db_index=True)
    # 股東會日期
    shareholder_meeting_date = models.DateField()
    # 本期淨利（淨損）(元)
    net_profit_after_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 可分配盈餘(元)
    distributable_net_profit = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 現金股利-盈餘(元/股)
    cash_dividends_earnings = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    # 現金股利-公積(元/股)
    cash_dividends_surplus = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    # 現金股利合計(元/股)
    cash_dividends_all = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    # 股票股利-盈餘(元/股)
    stock_dividends_earnings = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    # 股票股利-公積(元/股)
    stock_dividends_surplus = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    # 股票股利合計(元/股)
    stock_dividends_all = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    # 董監酬勞(元)
    payable_to_directors_and_supervisors = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 員工紅利-現金(元)
    employee_bonus_cash = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 員工紅利-股票(元)
    employee_bonus_stock = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 員工紅利合計(元)
    employee_bonus_all = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    modified_date = models.DateField(auto_now=True)

# 英文編名參考公開資訊觀測站英文版財報項目名稱
# 資產負債表(季)
class SeasonBalanceSheet(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    symbol = models.CharField(max_length=20, db_index=True)
    year = models.IntegerField(db_index=True)
    season = models.CharField(max_length=20, db_index=True)
    date = models.CharField(max_length=20, db_index=True)
    # 現金及約當現金
    total_cash_and_cash_equivalents = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 透過損益按公允價值衡量之金融資產－流動
    total_current_financial_assets_at_fair_value_through_profit_or_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 備供出售金融資產－流動淨額
    current_available_for_sale_financial_assets_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 持有至到期日金融資產－流動淨額
    current_held_to_maturity_financial_assets_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收票據淨額
    notes_receivable_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收帳款淨額
    accounts_receivable_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收帳款－關係人淨額
    accounts_receivable_due_from_related_parties_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他應收款淨額
    other_receivables_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他應收款－關係人淨額
    other_receivables_due_from_related_parties_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 存貨
    total_inventories = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 預付款項
    total_prepayments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他流動資產
    total_other_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 流動資產合計
    total_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 備供出售金融資產－非流動淨額
    non_current_available_for_sale_financial_assets_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 持有至到期日金融資產－非流動淨額
    non_current_held_to_maturity_financial_assets_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 避險之衍生金融資產－非流動
    derivative_non_current_financial_assets_for_hedging = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 以成本衡量之金融資產－非流動淨額
    non_current_financial_assets_at_cost_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 採用權益法之投資淨額
    investments_accounted_for_using_equity_method_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 不動產、廠房及設備
    total_property_plant_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 無形資產
    total_intangible_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 遞延所得稅資產
    deferred_tax_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他非流動資產
    total_other_non_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 非流動資產合計
    total_non_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 資產總額
    total_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 短期借款
    total_short_term_borrowings = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 透過損益按公允價值衡量之金融負債－流動
    total_current_financial_liabilities_at_fair_value_through_profit_or_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付短期票券
    total_short_term_notes_and_bills_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付帳款
    total_accounts_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付帳款－關係人
    total_accounts_payable_to_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他應付款
    total_other_payables = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 當期所得稅負債
    current_tax_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 負債準備－流動
    total_current_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他流動負債
    total_other_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 流動負債合計
    total_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付公司債
    total_bonds_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 長期借款
    total_long_borrowings = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 負債準備－非流動
    total_non_current_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 遞延所得稅負債
    total_deferred_tax_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他非流動負債
    total_other_non_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 非流動負債合計
    total_non_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 負債總額
    total_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 普通股股本
    ordinary_share = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 股本合計
    total_capital_stock = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 資本公積－發行溢價
    total_capital_surplus_additional_paid_in_capital = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 資本公積－取得或處分子公司股權價格與帳面價值差額
    capital_surplus_difference_between_consideration_and_carrying_amount_of_subsidiaries_acquired_or_disposed = models.DecimalField(
                                                                                            max_digits=20, decimal_places=0, null=True)
    # 資本公積－受贈資產
    total_capital_surplus_donated_assets_received = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 資本公積－採用權益法認列關聯企業及合資股權淨值之變動數
    capital_surplus_changes_in_equity_of_associates_and_joint_ventures_accounted_for_using_equity_method = models.DecimalField(
                                                                                            max_digits=20, decimal_places=0, null=True)
    # 資本公積－合併溢額
    capital_surplus_net_assets_from_merger = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 資本公積合計
    total_capital_surplus = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 法定盈餘公積
    legal_reserve = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 特別盈餘公積
    special_reserve = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 未分配盈餘（或待彌補虧損）
    total_unappropriated_retained_earnings_accumulated_deficit = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 保留盈餘合計
    total_retained_earnings = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他權益合計
    total_other_equity_interest = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 庫藏股票
    treasury_shares = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 歸屬於母公司業主之權益合計
    total_equity_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 非控制權益
    non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 權益總額
    total_equity = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 預收股款（權益項下）之約當發行股數（單位：股）
    equivalent_issue_shares_of_advance_receipts_for_ordinary_share = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 母公司暨子公司所持有之母公司庫藏股股數（單位：股）
    number_of_shares_in_entity_held_by_entity_and_by_its_subsidiaries = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.date, 
        self.total_cash_and_cash_equivalents, self.current_available_for_sale_financial_assets_net,
        self.notes_receivable_net, self.accounts_receivable_net, self.total_inventories,
        self.total_current_assets, self.investments_accounted_for_using_equity_method_net,
        self.total_property_plant_and_equipment, self.total_intangible_assets,
        self.total_non_current_assets, self.total_assets,
        self.total_short_term_borrowings, self.total_short_term_notes_and_bills_payable,
        self.total_accounts_payable, self.total_current_liabilities, self.total_bonds_payable,
        self.total_long_borrowings, self.total_non_current_liabilities, self.total_liabilities,
        self.ordinary_share, self.total_capital_surplus, self.total_retained_earnings,
        self.total_equity_attributable_to_owners_of_parent, self.total_equity,
        self.modified_date)
    class Meta:
        ordering = ['symbol', 'date']
    class Admin:
        pass

# 英文編名參考公開資訊觀測站英文版財報項目名稱
# 綜合損益表(季)
class SeasonIncomeStatement(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    symbol = models.CharField(max_length=20, db_index=True)
    year = models.IntegerField(db_index=True)
    season = models.CharField(max_length=20, db_index=True)
    date = models.CharField(max_length=20, db_index=True)
    # 銷貨收入淨額
    net_sales_revenue = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 勞務收入
    total_service_revenue = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業收入合計
    total_operating_revenue = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 銷貨成本
    total_cost_of_sales = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 勞務成本
    total_cost_of_services = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業成本合計
    total_operating_costs = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業毛利（毛損）
    gross_profit_loss_from_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業毛利（毛損）淨額
    gross_profit_loss_from_operations_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 推銷費用
    total_selling_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 管理費用
    total_administrative_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 研究發展費用
    total_research_and_development_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業費用合計
    total_operating_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業利益（損失）
    net_operating_income_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他收入
    total_other_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他利益及損失淨額
    other_gains_and_losses_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 財務成本淨額
    finance_costs_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業外收入及支出合計
    total_non_operating_income_and_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 稅前淨利（淨損）
    profit_loss_from_continuing_operations_before_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 所得稅費用（利益）合計
    total_tax_expense_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 繼續營業單位本期淨利（淨損）
    profit_loss_from_continuing_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 本期淨利（淨損）
    profit_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 國外營運機構財務報表換算之兌換差額
    exchange_differences_on_translation = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 備供出售金融資產未實現評價損益
    unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他綜合損益（淨額）
    other_comprehensive_income_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 本期綜合損益總額
    total_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 母公司業主（淨利／損）
    profit_loss_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 非控制權益（淨利／損）
    profit_loss_attributable_to_non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 母公司業主（綜合損益）
    comprehensive_income_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 非控制權益（綜合損益）
    comprehensive_income_attributable_to_non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 基本每股盈餘
    total_basic_earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 稀釋每股盈餘
    total_diluted_earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 營收年增率
    total_operating_revenue_yoy = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
    	return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.date, 
        	self.total_operating_revenue, self.gross_profit_loss_from_operations,
        	self.net_operating_income_loss, self.total_non_operating_income_and_expenses,
        	self.total_tax_expense_income, self.profit_loss, self.total_comprehensive_income,
        	self.profit_loss_attributable_to_owners_of_parent,
    		self.comprehensive_income_attributable_to_owners_of_parent,
    		self.total_basic_earnings_per_share, self.total_diluted_earnings_per_share,
            self.modified_date)
    class Meta:
        ordering = ['symbol', 'date']
    class Admin:
        pass

# 英文編名參考公開資訊觀測站英文版財報項目名稱
# 綜合損益表(年)
class AnnualIncomeStatement(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    symbol = models.CharField(max_length=20, db_index=True)
    year = models.IntegerField(db_index=True)
    # 銷貨收入淨額
    net_sales_revenue = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 勞務收入
    total_service_revenue = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業收入合計
    total_operating_revenue = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 銷貨成本
    total_cost_of_sales = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 勞務成本
    total_cost_of_services = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業成本合計
    total_operating_costs = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業毛利（毛損）
    gross_profit_loss_from_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業毛利（毛損）淨額
    gross_profit_loss_from_operations_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 推銷費用
    total_selling_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 管理費用
    total_administrative_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 研究發展費用
    total_research_and_development_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業費用合計
    total_operating_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業利益（損失）
    net_operating_income_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他收入
    total_other_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他利益及損失淨額
    other_gains_and_losses_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 財務成本淨額
    finance_costs_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業外收入及支出合計
    total_non_operating_income_and_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 稅前淨利（淨損）
    profit_loss_from_continuing_operations_before_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 所得稅費用（利益）合計
    total_tax_expense_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 繼續營業單位本期淨利（淨損）
    profit_loss_from_continuing_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 本期淨利（淨損）
    profit_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 國外營運機構財務報表換算之兌換差額
    exchange_differences_on_translation = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 備供出售金融資產未實現評價損益
    unrealised_gains_losses_on_valuation_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他綜合損益（淨額）
    other_comprehensive_income_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 本期綜合損益總額
    total_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 母公司業主（淨利／損）
    profit_loss_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 非控制權益（淨利／損）
    profit_loss_attributable_to_non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 母公司業主（綜合損益）
    comprehensive_income_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 非控制權益（綜合損益）
    comprehensive_income_attributable_to_non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 基本每股盈餘
    total_basic_earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 稀釋每股盈餘
    total_diluted_earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.year, 
            self.total_operating_revenue, self.gross_profit_loss_from_operations,
            self.net_operating_income_loss, self.total_non_operating_income_and_expenses,
            self.total_tax_expense_income, self.profit_loss, self.total_comprehensive_income,
            self.profit_loss_attributable_to_owners_of_parent,
            self.comprehensive_income_attributable_to_owners_of_parent,
            self.total_basic_earnings_per_share, self.total_diluted_earnings_per_share,
            self.modified_date)
    class Meta:
        ordering = ['symbol', 'year']
    class Admin:
        pass

# 英文編名參考公開資訊觀測站英文版財報項目名稱
# 現金流量表(季)
class SeasonCashFlow(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    symbol = models.CharField(max_length=20, db_index=True)
    year = models.IntegerField(db_index=True)
    season = models.CharField(max_length=20, db_index=True)
    date = models.CharField(max_length=20, db_index=True)
    # 繼續營業單位稅前淨利（淨損）
    profit_loss_from_continuing_operations_before_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 本期稅前淨利（淨損）
    profit_loss_before_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 折舊費用
    depreciation_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 攤銷費用
    amortization_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 透過損益按公允價值衡量金融資產及負債之淨損失（利益）
    net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 利息費用
    interest_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 利息收入
    interest_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 股份基礎給付酬勞成本
    share_based_payments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 採用權益法認列之關聯企業及合資損失（利益）之份額
    share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分及報廢不動產、廠房及設備損失（利益）
    loss_gain_on_disposal_of_property_plan_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分投資損失（利益）
    loss_gain_on_disposal_of_investments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分採用權益法之投資損失（利益）
    loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 已實現銷貨損失（利益）
    realized_loss_profit_on_from_sales = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 未實現外幣兌換損失（利益）
    unrealized_foreign_exchange_loss_gain = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他項目
    other_adjustments_to_reconcile_profit_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 不影響現金流量之收益費損項目合計
    total_adjustments_to_reconcile_profit_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 持有供交易之金融資產（增加）減少
    decrease_increase_in_financial_assets_held_for_trading = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 避險之衍生金融資產（增加）減少
    decrease_increase_in_derivative_financial_assets_for_hedging = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收票據（增加）減少
    decrease_increase_in_notes_receivable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收帳款（增加）減少
    decrease_increase_in_accounts_receivable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收帳款－關係人（增加）減少
    decrease_increase_in_accounts_receivable_due_from_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他應收款－關係人（增加）減少
    decrease_increase_in_other_receivable_due_from_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 存貨（增加）減少
    decrease_increase_in_inventories = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 預付款項（增加）減少
    decrease_increase_in_prepayments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他流動資產（增加）減少
    decrease_increase_in_other_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他金融資產（增加）減少
    decrease_increase_in_other_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他營業資產（增加）減少
    decrease_increase_in_other_operating_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 與營業活動相關之資產之淨變動合計
    total_changes_in_operating_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付帳款增加（減少）
    increase_decrease_in_accounts_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付帳款－關係人增加（減少）
    increase_decrease_in_accounts_payable_to_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他應付款增加（減少）
    increase_decrease_in_other_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 負債準備增加（減少）
    increase_decrease_in_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他流動負債增加（減少）
    increase_decrease_in_other_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應計退休金負債增加（減少）
    increase_decrease_in_accrued_pension_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 與營業活動相關之負債之淨變動合計
    total_changes_in_operating_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 與營業活動相關之資產及負債之淨變動合計
    total_changes_in_operating_assets_and_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 調整項目合計
    total_adjustments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營運產生之現金流入（流出）
    cash_inflow_outflow_generated_from_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 退還（支付）之所得稅
    income_taxes_refund_paid = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業活動之淨現金流入（流出）
    net_cash_flows_from_used_in_operating_activities = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 取得備供出售金融資產
    acquisition_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分備供出售金融資產
    proceeds_from_disposal_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 持有至到期日金融資產到期還本
    proceeds_from_repayments_of_held_to_maturity_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 取得以成本衡量之金融資產
    acquisition_of_financial_assets_at_cost = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分以成本衡量之金融資產
    proceeds_from_disposal_of_financial_assets_at_cost = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 取得不動產、廠房及設備
    acquisition_of_property_plant_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分不動產、廠房及設備
    proceeds_from_disposal_of_property_plant_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 取得無形資產
    acquisition_of_intangible_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他非流動資產增加
    increase_in_other_non_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 投資活動之淨現金流入（流出）
    net_cash_flows_from_used_in_investing_activities = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 短期借款增加
    increase_in_short_term_loans = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 短期借款減少
    decrease_in_short_term_loans = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付短期票券增加
    increase_in_short_term_notes_and_bills_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付短期票券減少
    decrease_in_short_term_notes_and_bills_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 發行公司債
    proceeds_from_issuing_bonds = models.DecimalField(max_digits=20, decimal_places=0, null=True)   
    # 償還公司債
    repayments_of_bonds = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 舉借長期借款
    proceeds_from_long_term_debt = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 償還長期借款
    repayments_of_long_term_debt = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 庫藏股票買回成本
    payments_to_acquire_treasury_shares = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 庫藏股票處分
    proceeds_from_sale_of_treasury_shares = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 發放現金股利
    cash_dividends_paid = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 籌資活動之淨現金流入（流出）
    net_cash_flows_from_used_in_financing_activities = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 匯率變動對現金及約當現金之影響
    effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 本期現金及約當現金增加（減少）數
    net_increase_decrease_in_cash_and_cash_equivalents = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 期初現金及約當現金餘額
    cash_and_cash_equivalents_at_beginning_of_period = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 期末現金及約當現金餘額
    cash_and_cash_equivalents_at_end_of_period = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 資產負債表帳列之現金及約當現金
    cash_and_cash_equivalents_reported_in_the_statement_of_financial_position = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 自由現金流量
    free_cash_flow = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.date, 
            self.profit_loss_before_tax, self.depreciation_expense, self.unrealized_foreign_exchange_loss_gain,
            self.income_taxes_refund_paid, self.net_cash_flows_from_used_in_operating_activities,
            self.net_cash_flows_from_used_in_investing_activities, self.net_cash_flows_from_used_in_financing_activities,
            self.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents,
            self.net_increase_decrease_in_cash_and_cash_equivalents,self.cash_and_cash_equivalents_at_end_of_period,
            self.free_cash_flow ,self.modified_date)
    class Meta:
        ordering = ['symbol', 'date']
    class Admin:
        pass

# 英文編名參考公開資訊觀測站英文版財報項目名稱
# 現金流量表(年)
class AnnualCashFlow(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    symbol = models.CharField(max_length=20, db_index=True)
    year = models.IntegerField(db_index=True)
    # 繼續營業單位稅前淨利（淨損）
    profit_loss_from_continuing_operations_before_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 本期稅前淨利（淨損）
    profit_loss_before_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 折舊費用
    depreciation_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 攤銷費用
    amortization_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 透過損益按公允價值衡量金融資產及負債之淨損失（利益）
    net_loss_gain_on_financial_assets_or_liabilities_at_fair_value_through_profit_or_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 利息費用
    interest_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 利息收入
    interest_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 股份基礎給付酬勞成本
    share_based_payments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 採用權益法認列之關聯企業及合資損失（利益）之份額
    share_of_loss_profit_of_associates_and_joint_ventures_accounted_for_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分及報廢不動產、廠房及設備損失（利益）
    loss_gain_on_disposal_of_property_plan_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分投資損失（利益）
    loss_gain_on_disposal_of_investments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分採用權益法之投資損失（利益）
    loss_gain_on_disposal_of_investments_accounted_for_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 已實現銷貨損失（利益）
    realized_loss_profit_on_from_sales = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 未實現外幣兌換損失（利益）
    unrealized_foreign_exchange_loss_gain = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他項目
    other_adjustments_to_reconcile_profit_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 不影響現金流量之收益費損項目合計
    total_adjustments_to_reconcile_profit_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 持有供交易之金融資產（增加）減少
    decrease_increase_in_financial_assets_held_for_trading = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 避險之衍生金融資產（增加）減少
    decrease_increase_in_derivative_financial_assets_for_hedging = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收票據（增加）減少
    decrease_increase_in_notes_receivable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收帳款（增加）減少
    decrease_increase_in_accounts_receivable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應收帳款－關係人（增加）減少
    decrease_increase_in_accounts_receivable_due_from_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他應收款－關係人（增加）減少
    decrease_increase_in_other_receivable_due_from_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 存貨（增加）減少
    decrease_increase_in_inventories = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 預付款項（增加）減少
    decrease_increase_in_prepayments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他流動資產（增加）減少
    decrease_increase_in_other_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他金融資產（增加）減少
    decrease_increase_in_other_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他營業資產（增加）減少
    decrease_increase_in_other_operating_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 與營業活動相關之資產之淨變動合計
    total_changes_in_operating_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付帳款增加（減少）
    increase_decrease_in_accounts_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付帳款－關係人增加（減少）
    increase_decrease_in_accounts_payable_to_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他應付款增加（減少）
    increase_decrease_in_other_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 負債準備增加（減少）
    increase_decrease_in_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他流動負債增加（減少）
    increase_decrease_in_other_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應計退休金負債增加（減少）
    increase_decrease_in_accrued_pension_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 與營業活動相關之負債之淨變動合計
    total_changes_in_operating_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 與營業活動相關之資產及負債之淨變動合計
    total_changes_in_operating_assets_and_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 調整項目合計
    total_adjustments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營運產生之現金流入（流出）
    cash_inflow_outflow_generated_from_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 退還（支付）之所得稅
    income_taxes_refund_paid = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 營業活動之淨現金流入（流出）
    net_cash_flows_from_used_in_operating_activities = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 取得備供出售金融資產
    acquisition_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分備供出售金融資產
    proceeds_from_disposal_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 持有至到期日金融資產到期還本
    proceeds_from_repayments_of_held_to_maturity_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 取得以成本衡量之金融資產
    acquisition_of_financial_assets_at_cost = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分以成本衡量之金融資產
    proceeds_from_disposal_of_financial_assets_at_cost = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 取得不動產、廠房及設備
    acquisition_of_property_plant_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 處分不動產、廠房及設備
    proceeds_from_disposal_of_property_plant_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 取得無形資產
    acquisition_of_intangible_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 其他非流動資產增加
    increase_in_other_non_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 投資活動之淨現金流入（流出）
    net_cash_flows_from_used_in_investing_activities = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 短期借款增加
    increase_in_short_term_loans = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 短期借款減少
    decrease_in_short_term_loans = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付短期票券增加
    increase_in_short_term_notes_and_bills_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 應付短期票券減少
    decrease_in_short_term_notes_and_bills_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 發行公司債
    proceeds_from_issuing_bonds = models.DecimalField(max_digits=20, decimal_places=0, null=True)   
    # 償還公司債
    repayments_of_bonds = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 舉借長期借款
    proceeds_from_long_term_debt = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 償還長期借款
    repayments_of_long_term_debt = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 庫藏股票買回成本
    payments_to_acquire_treasury_shares = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 庫藏股票處分
    proceeds_from_sale_of_treasury_shares = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 發放現金股利
    cash_dividends_paid = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 籌資活動之淨現金流入（流出）
    net_cash_flows_from_used_in_financing_activities = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 匯率變動對現金及約當現金之影響
    effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 本期現金及約當現金增加（減少）數
    net_increase_decrease_in_cash_and_cash_equivalents = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 期初現金及約當現金餘額
    cash_and_cash_equivalents_at_beginning_of_period = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 期末現金及約當現金餘額
    cash_and_cash_equivalents_at_end_of_period = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    # 資產負債表帳列之現金及約當現金
    cash_and_cash_equivalents_reported_in_the_statement_of_financial_position = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    # 自由現金流量
    free_cash_flow = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.year, 
            self.profit_loss_before_tax, self.depreciation_expense, self.unrealized_foreign_exchange_loss_gain,
            self.income_taxes_refund_paid, self.net_cash_flows_from_used_in_operating_activities,
            self.net_cash_flows_from_used_in_investing_activities, self.net_cash_flows_from_used_in_financing_activities,
            self.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents,
            self.net_increase_decrease_in_cash_and_cash_equivalents,self.cash_and_cash_equivalents_at_end_of_period,
            self.free_cash_flow, self.modified_date)
    class Meta:
        ordering = ['symbol', 'year']
    class Admin:
        pass

# 財務比率表(季)
class SeasonFinancialRatio(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    symbol = models.CharField(max_length=20, db_index=True)
    year = models.IntegerField(db_index=True)
    season = models.CharField(max_length=20, db_index=True)
    date = models.CharField(max_length=20, db_index=True)
    # ---獲利能力---
    # 毛利率
    gross_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 營益率
    operating_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 稅前淨利率
    net_profit_margin_before_tax = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 稅後淨利率
    net_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 每股盈餘(EPS)
    earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 總資產報酬率(ROA)
    return_on_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 股東權益報酬率(ROE)
    return_on_equity = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # ---償債能力---
    # 流動比率
    current_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 速動比率
    quick_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 金融負債比率
    financial_debt_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 負債比率
    debt_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # ---經營能力---
    # 應收帳款週轉率
    accounts_receivable_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 存貨週轉率
    inventory_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 固定資產週轉率
    fixed_asset_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 總資產週轉率
    total_asset_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # ---黃國華指標---
    # 存貨營收比
    inventory_sales_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 備供出售比率
    available_for_sale_to_equity_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 無形資產比率
    intangible_asset_to_equity_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 未折舊比率
    undepreciation_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 折舊負擔比率
    depreciation_to_sales_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 營業利益佔稅前淨利比率
    operating_profit_to_net_profit_before_tax_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 現金股息配發率
    payout_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 營業稅率
    tax_rate = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.date, 
            self.gross_profit_margin, self.operating_profit_margin, self.net_profit_margin,
            self.earnings_per_share, self.return_on_assets, self.return_on_equity,
            self.current_ratio, self.quick_ratio, self.financial_debt_ratio, self.debt_ratio,
            self.accounts_receivable_turnover_ratio, self.inventory_turnover_ratio,
            self.fixed_asset_turnover_ratio, self.total_asset_turnover_ratio,
            self.inventory_sales_ratio,self.available_for_sale_to_equity_ratio,
            self.intangible_asset_to_equity_ratio,self.undepreciation_ratio,
            self.depreciation_to_sales_ratio,self.operating_profit_to_net_profit_before_tax_ratio,
            self.payout_ratio , self.tax_rate ,self.modified_date)
    class Meta:
        ordering = ['symbol', 'date']
    class Admin:
        pass

# 財務比率表(年)
class AnnualFinancialRatio(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    symbol = models.CharField(max_length=20, db_index=True)
    year = models.IntegerField(db_index=True)
    # ---獲利能力---
    # 毛利率
    gross_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 營益率
    operating_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 稅前淨利率
    net_profit_margin_before_tax = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 稅後淨利率
    net_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 每股盈餘(EPS)
    earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 總資產報酬率(ROA)
    return_on_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 股東權益報酬率(ROE)
    return_on_equity = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # ---償債能力---
    # 流動比率
    current_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 速動比率
    quick_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 金融負債比率
    financial_debt_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 負債比率
    debt_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # ---經營能力---
    # 應收帳款週轉率
    accounts_receivable_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 存貨週轉率
    inventory_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 固定資產週轉率
    fixed_asset_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 總資產週轉率
    total_asset_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # ---黃國華指標---
    # 存貨營收比
    inventory_sales_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 備供出售比率
    available_for_sale_to_equity_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 無形資產比率
    intangible_asset_to_equity_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 未折舊比率
    undepreciation_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 折舊負擔比率
    depreciation_to_sales_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 營業利益佔稅前淨利比率
    operating_profit_to_net_profit_before_tax_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 現金股息配發率
    payout_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    # 營業稅率
    tax_rate = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.year, 
            self.gross_profit_margin, self.operating_profit_margin, self.net_profit_margin,
            self.earnings_per_share, self.return_on_assets, self.return_on_equity,
            self.current_ratio, self.quick_ratio, self.financial_debt_ratio, self.debt_ratio,
            self.accounts_receivable_turnover_ratio, self.inventory_turnover_ratio,
            self.fixed_asset_turnover_ratio, self.total_asset_turnover_ratio,
            self.inventory_sales_ratio,self.available_for_sale_to_equity_ratio,
            self.intangible_asset_to_equity_ratio,self.undepreciation_ratio,
            self.depreciation_to_sales_ratio,self.operating_profit_to_net_profit_before_tax_ratio,
            self.payout_ratio , self.tax_rate ,self.modified_date)
    class Meta:
        ordering = ['symbol', 'year']
    class Admin:
        pass