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
)
urlpatterns += patterns('pickstock.pickstock_views',
	url(r'^pickstock_home/$', 'pickstock_home'),
	url(r'^pickstock_bluechip/$', 'pickstock_bluechip'),
)

