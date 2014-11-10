#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'pickstock.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^admin/', include(admin.site.urls)),
)

# These urls are used to update data, like stockid, price, sales, and financial reports
urlpatterns += patterns('stockid.views',
	url(r'^updateid/$', 'get_stockid'),
)
urlpatterns += patterns('stockprice.views',
	url(r'^updateprice/$', 'get_stockprice'),
	url(r'^updatedailyprice/$', 'get_latest_stockprice'),
)
urlpatterns += patterns('stocksales.views',
	url(r'^updatesales/$', 'get_IFRS_sales'),
)
urlpatterns += patterns('stockfins.views',
	url(r'^updatefins-bs/$', 'season_balance_sheet'),
	url(r'^updatefins-is/$', 'season_income_statement'),
	url(r'^updatefins-is-annual/$', 'annual_income_statement'),
	url(r'^updatefins-cf/$', 'season_cash_flow'),
	url(r'^updatefins-cf-annual/$', 'annual_cash_flow'),
	url(r'^updatefins-fr/$', 'season_financial_ratio'),
	url(r'^updatefins-fr-annual/$', 'annual_financial_ratio'),
	url(r'^updatefins-payout/$', 'earnings_payout'),
	url(r'^update_season_all/$', 'update_season_all'),
	url(r'^update_annual_all/$', 'update_annual_all'),
)
urlpatterns += patterns('stockchip.views',
	url(r'^updatechip_bigchip/$', 'updatechip_bigchip'),
)
urlpatterns += patterns('economics.views',
	url(r'^tw_indicators/$', 'tw_indicators'),
)

#main page(DO NOT USE THESE FILE TO TEST ANYTHING!!!)
urlpatterns += patterns('pickstock.sales_views',
	url(r'^home/$', 'home'),
	url(r'^update/$', 'update'),
	url(r'^assign_task/$', 'assign_task'),
	url(r'^sales_overview/$', 'sales_overview'),
	url(r'^season_effect/$', 'season_effect'),
	url(r'^price_momentum/$', 'price_momentum'),
	url(r'^basic_overview/$', 'basic_overview'),
	url(r'^defensive_indicator/$', 'defensive_indicator'),
	url(r'^potentialrisk_indicator/$', 'potentialrisk_indicator'),
	url(r'^profitable_indicator_1/$', 'profitable_indicator_1'),
	url(r'^profitable_indicator_2/$', 'profitable_indicator_2'),
	url(r'^stability_indicator/$', 'stability_indicator'),
	url(r'^cashflow_indicator/$', 'cashflow_indicator'),
	url(r'^bigchip_tracking/$', 'bigchip_tracking'),
	url(r'^bigchip_tracking_chart/$', 'bigchip_tracking_chart'),
)
urlpatterns += patterns('pickstock.economics_views',
	url(r'^tw_economics_home/$', 'tw_economics_home'),
	url(r'^tw_economics/$', 'tw_economics'),
	url(r'^usa_economics_home/$', 'usa_economics_home'),
	url(r'^world_economics_home/$', 'world_economics_home'),

	url(r'^usa_economics_real_gdp_contribution/$', 'usa_economics_real_gdp_contribution'),
	url(r'^usa_economics_real_pce_contribution/$', 'usa_economics_real_pce_contribution'),
	url(r'^usa_economics_real_pcdg_contribution/$', 'usa_economics_real_pcdg_contribution'),
	url(r'^usa_economics_real_gpdi_contribution/$', 'usa_economics_real_gpdi_contribution'),
	url(r'^usa_economics_real_prfi_contribution/$', 'usa_economics_real_prfi_contribution'),
	url(r'^usa_economics_real_pnfi_contribution/$', 'usa_economics_real_pnfi_contribution'),
	url(r'^usa_economics_real_impgs_contribution/$', 'usa_economics_real_impgs_contribution'),
	url(r'^usa_economics_real_expgs_contribution/$', 'usa_economics_real_expgs_contribution'),
	url(r'^usa_economics_real_gce_contribution/$', 'usa_economics_real_gce_contribution'),

	url(r'^usa_economics_real_gdp_amount/$', 'usa_economics_real_gdp_amount'),
	url(r'^usa_economics_real_pce_amount/$', 'usa_economics_real_pce_amount'),
	url(r'^usa_economics_real_pcdg_amount/$', 'usa_economics_real_pcdg_amount'),
	url(r'^usa_economics_real_gpdi_amount/$', 'usa_economics_real_gpdi_amount'),
	url(r'^usa_economics_real_prfi_amount/$', 'usa_economics_real_prfi_amount'),
	url(r'^usa_economics_real_pnfi_amount/$', 'usa_economics_real_pnfi_amount'),
	url(r'^usa_economics_real_impgs_amount/$', 'usa_economics_real_impgs_amount'),
	url(r'^usa_economics_real_expgs_amount/$', 'usa_economics_real_expgs_amount'),
	url(r'^usa_economics_real_gce_amount/$', 'usa_economics_real_gce_amount'),
	
	url(r'^usa_economics_real_gdp/$', 'usa_economics_real_gdp'),
	url(r'^usa_economics_dollar_gdp/$', 'usa_economics_dollar_gdp'),
	url(r'^usa_economics_real_pce/$', 'usa_economics_real_pce'),
	url(r'^usa_economics_real_pcdg/$', 'usa_economics_real_pcdg'),
	url(r'^usa_economics_real_gpdi/$', 'usa_economics_real_gpdi'),
	url(r'^usa_economics_real_prfi/$', 'usa_economics_real_prfi'),
	url(r'^usa_economics_real_pnfi/$', 'usa_economics_real_pnfi'),
	url(r'^usa_economics_real_impgs/$', 'usa_economics_real_impgs'),
	url(r'^usa_economics_real_expgs/$', 'usa_economics_real_expgs'),
	url(r'^usa_economics_real_gce/$', 'usa_economics_real_gce'),
	url(r'^usa_economics_dollar_dpi/$', 'usa_economics_dollar_dpi'),

	url(r'^usa_economics_civilian_unemployment_rate/$', 'usa_economics_civilian_unemployment_rate'),
	url(r'^usa_economics_civilians_unemployed_lt5/$', 'usa_economics_civilians_unemployed_lt5'),
	url(r'^usa_economics_civilians_unemployed_5to14/$', 'usa_economics_civilians_unemployed_5to14'),
	url(r'^usa_economics_civilians_unemployed_15t26/$', 'usa_economics_civilians_unemployed_15t26'),
	url(r'^usa_economics_civilians_unemployed_27ov/$', 'usa_economics_civilians_unemployed_27ov'),
	url(r'^usa_economics_sp500_index_monthly/$', 'usa_economics_sp500_index_monthly'),

	url(r'^usa_economics_dollar_cpi/$', 'usa_economics_dollar_cpi'),
	url(r'^usa_economics_core_cpi/$', 'usa_economics_core_cpi'),
	url(r'^usa_economics_10yr_yield/$', 'usa_economics_10yr_yield'),
	url(r'^usa_economics_30yr_mortg_rate/$', 'usa_economics_30yr_mortg_rate'),

	url(r'^usa_economics_us_dollar_index/$', 'usa_economics_us_dollar_index'),
	url(r'^usa_economics_euro_exchange_rate/$', 'usa_economics_euro_exchange_rate'),
	url(r'^usa_economics_jpy_exchange_rate/$', 'usa_economics_jpy_exchange_rate'),
	url(r'^usa_economics_cny_exchange_rate/$', 'usa_economics_cny_exchange_rate'),
	url(r'^usa_economics_twd_exchange_rate/$', 'usa_economics_twd_exchange_rate'),
	url(r'^usa_economics_krw_exchange_rate/$', 'usa_economics_krw_exchange_rate'),
	url(r'^usa_economics_aud_exchange_rate/$', 'usa_economics_aud_exchange_rate'),
	url(r'^usa_economics_cboe_vix_index/$', 'usa_economics_cboe_vix_index'),

	url(r'^world_real_gdp_usa/$', 'world_real_gdp_usa'),
	url(r'^world_real_gdp_eurozone/$', 'world_real_gdp_eurozone'),
	url(r'^world_real_gdp_china/$', 'world_real_gdp_china'),
	url(r'^world_real_gdp_japan/$', 'world_real_gdp_japan'),
	url(r'^world_real_gdp_germany/$', 'world_real_gdp_germany'),
	url(r'^world_real_gdp_france/$', 'world_real_gdp_france'),
	url(r'^world_real_gdp_uk/$', 'world_real_gdp_uk'),
	url(r'^world_real_gdp_brazil/$', 'world_real_gdp_brazil'),
	url(r'^world_real_gdp_italy/$', 'world_real_gdp_italy'),
	url(r'^world_real_gdp_india/$', 'world_real_gdp_india'),
)
urlpatterns += patterns('pickstock.pickstock_views',
	url(r'^pickstock_home/$', 'pickstock_home'),
	url(r'^pickstock_bluechip/$', 'pickstock_bluechip'),
)

