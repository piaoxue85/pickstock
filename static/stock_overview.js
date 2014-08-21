$(document).ready(function() {
	basic_overview();
	profitable_indicator_1();
	$("li#defensive_indicator").click(function() {
		defensive_indicator();
	});
	$("li#potentialrisk_indicator").click(function() {
		potentialrisk_indicator();
	})
	$("li#profitable_indicator_1").click(function() {
		profitable_indicator_1();
	});
	$("li#profitable_indicator_2").click(function() {
		profitable_indicator_2();
	});
	$("li#stability_indicator").click(function() {
		stability_indicator();
	});
	$("li#cashflow_indicator").click(function() {
		cashflow_indicator();
	});
});

//將數字轉成帶有千分位符號的格式
function number_format(n) {
    n += "";
    var arr = n.split(".");
    var re = /(\d{1,3})(?=(\d{3})+$)/g;
    return arr[0].replace(re,"$1,") + (arr.length == 2 ? "."+arr[1] : "");
};

function basic_overview() {
	$.ajax({
		url:"/basic_overview/",
		type: "GET",
		dataType: "json",
		success: function(data) {
			console.log(data);
			// 季度
			var i = 0;
			$.each(data.quarter_name, function() {
				$("#quarter_name").append(
					"<th style='text-align:center'>" + data.quarter_name[i] + "</th>"
				);
				i++;
			});
			// 營業收入(仟元)
			var i = 0;
			$.each(data.total_operating_revenue, function() {
				$("#total_operating_revenue").append(
					"<td style='text-align:center'>" + number_format(data.total_operating_revenue[i]) + "</td>"
				);
				i++;
			});
			// 營收年增率
			var i = 0;
			$.each(data.total_operating_revenue_yoy, function() {
				$("#total_operating_revenue_yoy").append(
					"<td style='text-align:center'>" + data.total_operating_revenue_yoy[i] + "</td>"
				);
				i++;
			});
			// 應收帳款週轉率
			var i = 0;
			$.each(data.accounts_receivable_turnover_ratio, function() {
				$("#accounts_receivable_turnover_ratio").append(
					"<td style='text-align:center'>" + data.accounts_receivable_turnover_ratio[i] + "</td>"
				);
				i++;
			});
			// 存貨週轉率
			var i = 0;
			$.each(data.inventory_turnover_ratio, function() {
				$("#inventory_turnover_ratio").append(
					"<td style='text-align:center'>" + data.inventory_turnover_ratio[i] + "</td>"
				);
				i++;
			});
			// 存貨營收比
			var i = 0;
			$.each(data.inventory_sales_ratio, function() {
				$("#inventory_sales_ratio").append(
					"<td style='text-align:center'>" + data.inventory_sales_ratio[i] + "</td>"
				);
				i++;
			});
			// 備供出售比率
			var i = 0;
			$.each(data.available_for_sale_to_equity_ratio, function() {
				$("#available_for_sale_to_equity_ratio").append(
					"<td style='text-align:center'>" + data.available_for_sale_to_equity_ratio[i] + "</td>"
				);
				i++;
			});
			// 金融負債比率
			var i = 0;
			$.each(data.financial_debt_ratio, function() {
				$("#financial_debt_ratio").append(
					"<td style='text-align:center'>" + data.financial_debt_ratio[i] + "</td>"
				);
				i++;
			});
			// 無形資產比率
			var i = 0;
			$.each(data.intangible_asset_to_equity_ratio, function() {
				$("#intangible_asset_to_equity_ratio").append(
					"<td style='text-align:center'>" + data.intangible_asset_to_equity_ratio[i] + "</td>"
				);
				i++;
			});
			// 固定資產
			var i = 0;
			$.each(data.total_property_plant_and_equipment, function() {
				$("#total_property_plant_and_equipment").append(
					"<td style='text-align:center'>" + number_format(data.total_property_plant_and_equipment[i]) + "</td>"
				);
				i++;
			});
			// 固定資產週轉率
			var i = 0;
			$.each(data.fixed_asset_turnover_ratio, function() {
				$("#fixed_asset_turnover_ratio").append(
					"<td style='text-align:center'>" + data.fixed_asset_turnover_ratio[i] + "</td>"
				);
				i++;
			});
			// 折舊費用
			var i = 0;
			$.each(data.depreciation_expense, function() {
				$("#depreciation_expense").append(
					"<td style='text-align:center'>" + number_format(data.depreciation_expense[i]) + "</td>"
				);
				i++;
			});
			// 折舊負擔比率
			var i = 0;
			$.each(data.depreciation_to_sales_ratio, function() {
				$("#depreciation_to_sales_ratio").append(
					"<td style='text-align:center'>" + data.depreciation_to_sales_ratio[i] + "</td>"
				);
				i++;
			});
			// 營業毛利率
			var i = 0;
			$.each(data.gross_profit_margin, function() {
				$("#gross_profit_margin").append(
					"<td style='text-align:center'>" + data.gross_profit_margin[i] + "</td>"
				);
				i++;
			});
			// 營業利益率
			var i = 0;
			$.each(data.operating_profit_margin, function() {
				$("#operating_profit_margin").append(
					"<td style='text-align:center'>" + data.operating_profit_margin[i] + "</td>"
				);
				i++;
			});
			// 每股盈餘EPS
			var i = 0;
			$.each(data.earnings_per_share, function() {
				$("#earnings_per_share").append(
					"<td style='text-align:center'>" + data.earnings_per_share[i] + "</td>"
				);
				i++;
			});
			// 營業利益(仟元)
			var i = 0;
			$.each(data.net_operating_income_loss, function() {
				$("#net_operating_income_loss").append(
					"<td style='text-align:center'>" + number_format(data.net_operating_income_loss[i]) + "</td>"
				);
				i++;
			});
			// 本業獲利比重
			var i = 0;
			$.each(data.operating_profit_to_net_profit_before_tax_ratio, function() {
				$("#operating_profit_to_net_profit_before_tax_ratio").append(
					"<td style='text-align:center'>" + data.operating_profit_to_net_profit_before_tax_ratio[i] + "</td>"
				);
				i++;
			});
			// 營運現金流量
			var i = 0;
			$.each(data.net_cash_flows_from_used_in_operating_activities, function() {
				$("#net_cash_flows_from_used_in_operating_activities").append(
					"<td style='text-align:center'>" + number_format(data.net_cash_flows_from_used_in_operating_activities[i]) + "</td>"
				);
				i++;
			});
			// 投資現金流量
			var i = 0;
			$.each(data.net_cash_flows_from_used_in_investing_activities, function() {
				$("#net_cash_flows_from_used_in_investing_activities").append(
					"<td style='text-align:center'>" + number_format(data.net_cash_flows_from_used_in_investing_activities[i]) + "</td>"
				);
				i++;
			});
			// 自由現金流量
			var i = 0;
			$.each(data.free_cash_flow, function() {
				$("#free_cash_flow").append(
					"<td style='text-align:center'>" + number_format(data.free_cash_flow[i]) + "</td>"
				);
				i++;
			});
			// 所得稅率
			var i = 0;
			$.each(data.tax_rate, function() {
				$("#tax_rate").append(
					"<td style='text-align:center'>" + data.tax_rate[i]   + "</td>"
				);
				i++;
			});
			// 普通股股本(仟股)
			var i = 0;
			$.each(data.ordinary_share, function() {
				$("#ordinary_share").append(
					"<td style='text-align:center'>" + number_format(data.ordinary_share[i])   + "</td>"
				);
				i++;
			});
		},
		error: function() {
			alert("ERROR!!!");
		}
	});
};

/**
 * Dark theme for Highcharts JS
 * @author Torstein Honsi
 * 以下這部分是Highchart的theme範本，直接上網站複製貼上即可使用
 */

// Load the fonts
Highcharts.createElement('link', {
   href: 'http://fonts.googleapis.com/css?family=Unica+One',
   rel: 'stylesheet',
   type: 'text/css'
}, null, document.getElementsByTagName('head')[0]);

Highcharts.theme = {
   colors: ["#2b908f", "#90ee7e", "#f45b5b", "#7798BF", "#aaeeee", "#ff0066", "#eeaaee",
      "#55BF3B", "#DF5353", "#7798BF", "#aaeeee"],
   chart: {
      backgroundColor: {
         linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
         stops: [
            [0, '#2a2a2b'],
            [1, '#3e3e40']
         ]
      },
      style: {
         fontFamily: "'Unica One', sans-serif"
      },
      plotBorderColor: '#606063'
   },
   title: {
      style: {
         color: '#E0E0E3',
         textTransform: 'uppercase',
         fontSize: '20px'
      }
   },
   subtitle: {
      style: {
         color: '#E0E0E3',
         textTransform: 'uppercase'
      }
   },
   xAxis: {
      gridLineColor: '#707073',
      labels: {
         style: {
            color: '#E0E0E3'
         }
      },
      lineColor: '#707073',
      minorGridLineColor: '#505053',
      tickColor: '#707073',
      title: {
         style: {
            color: '#A0A0A3'

         }
      }
   },
   yAxis: {
      gridLineColor: '#707073',
      labels: {
         style: {
            color: '#E0E0E3'
         }
      },
      lineColor: '#707073',
      minorGridLineColor: '#505053',
      tickColor: '#707073',
      tickWidth: 1,
      title: {
         style: {
            color: '#A0A0A3'
         }
      }
   },
   tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.85)',
      style: {
         color: '#F0F0F0'
      }
   },
   plotOptions: {
      series: {
         dataLabels: {
            color: '#B0B0B3'
         },
         marker: {
            lineColor: '#333'
         }
      },
      boxplot: {
         fillColor: '#505053'
      },
      candlestick: {
         lineColor: 'white'
      },
      errorbar: {
         color: 'white'
      }
   },
   legend: {
      itemStyle: {
         color: '#E0E0E3'
      },
      itemHoverStyle: {
         color: '#FFF'
      },
      itemHiddenStyle: {
         color: '#606063'
      }
   },
   credits: {
      style: {
         color: '#666'
      }
   },
   labels: {
      style: {
         color: '#707073'
      }
   },

   drilldown: {
      activeAxisLabelStyle: {
         color: '#F0F0F3'
      },
      activeDataLabelStyle: {
         color: '#F0F0F3'
      }
   },

   navigation: {
      buttonOptions: {
         symbolStroke: '#DDDDDD',
         theme: {
            fill: '#505053'
         }
      }
   },

   // scroll charts
   rangeSelector: {
      buttonTheme: {
         fill: '#505053',
         stroke: '#000000',
         style: {
            color: '#CCC'
         },
         states: {
            hover: {
               fill: '#707073',
               stroke: '#000000',
               style: {
                  color: 'white'
               }
            },
            select: {
               fill: '#000003',
               stroke: '#000000',
               style: {
                  color: 'white'
               }
            }
         }
      },
      inputBoxBorderColor: '#505053',
      inputStyle: {
         backgroundColor: '#333',
         color: 'silver'
      },
      labelStyle: {
         color: 'silver'
      }
   },

   navigator: {
      handles: {
         backgroundColor: '#666',
         borderColor: '#AAA'
      },
      outlineColor: '#CCC',
      maskFill: 'rgba(255,255,255,0.1)',
      series: {
         color: '#7798BF',
         lineColor: '#A6C7ED'
      },
      xAxis: {
         gridLineColor: '#505053'
      }
   },

   scrollbar: {
      barBackgroundColor: '#808083',
      barBorderColor: '#808083',
      buttonArrowColor: '#CCC',
      buttonBackgroundColor: '#606063',
      buttonBorderColor: '#606063',
      rifleColor: '#FFF',
      trackBackgroundColor: '#404043',
      trackBorderColor: '#404043'
   },

   // special colors for some of the
   legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
   background2: '#505053',
   dataLabelsColor: '#B0B0B3',
   textColor: '#C0C0C0',
   contrastTextColor: '#F0F0F3',
   maskColor: 'rgba(255,255,255,0.3)'
};

/**
 * Experimental Highcharts plugin to implement chart.alignThreshold option.
 * Author: Torstein Hønsi
 * Last revision: 2013-12-02
 * 以下這部分是Highchart的plugin，可以把多個Y軸的0對準在同一水平，直接複製貼上即可使用
 */
(function (H) {
    var each = H.each;
    H.wrap(H.Chart.prototype, 'adjustTickAmounts', function (proceed) {
        var ticksBelowThreshold = 0,
            ticksAboveThreshold = 0;
        if (this.options.chart.alignThresholds) {
            each(this.yAxis, function (axis) {
                var threshold = axis.series[0] && axis.series[0].options.threshold || 0,
                    index = axis.tickPositions && axis.tickPositions.indexOf(threshold);

                if (index !== undefined && index !== -1) {
                    axis.ticksBelowThreshold = index;
                    axis.ticksAboveThreshold = axis.tickPositions.length - index;
                    ticksBelowThreshold = Math.max(ticksBelowThreshold, index);
                    ticksAboveThreshold = Math.max(ticksAboveThreshold, axis.ticksAboveThreshold);
                }
            });

            each(this.yAxis, function (axis) {
                
                var tickPositions = axis.tickPositions;

                if (tickPositions) {

                    if (axis.ticksAboveThreshold < ticksAboveThreshold) {
                        while (axis.ticksAboveThreshold < ticksAboveThreshold) {
                            tickPositions.push(
                                tickPositions[tickPositions.length - 1] + axis.tickInterval
                            );
                            axis.ticksAboveThreshold++;
                        }
                    }

                    if (axis.ticksBelowThreshold < ticksBelowThreshold) {
                        while (axis.ticksBelowThreshold < ticksBelowThreshold) {
                            tickPositions.unshift(
                                tickPositions[0] - axis.tickInterval
                            );
                            axis.ticksBelowThreshold++;
                        }

                    }
                    //axis.transA *= (calculatedTickAmount - 1) / (tickAmount - 1);
                    axis.min = tickPositions[0];
                    axis.max = tickPositions[tickPositions.length - 1];
                }
            });
        } else {
            proceed.call(this);
        }

    })
}(Highcharts));

function defensive_indicator() {
    $.getJSON("/defensive_indicator/", function (data) {
        // 載入Highchart Dark-unica theme
        Highcharts.setOptions(Highcharts.theme);
        // 貼上HighChart的程式碼
        $('.container#chart').highcharts({
	        chart: {
	            zoomType: 'xy'
	        },
	        title: {
	            text: '應收帳款週轉率/防禦性指標 vs 營業收入'
	        },
	        subtitle: {
	            text: 'Source: 公開資訊觀測站'
	        },
	        xAxis: [{
	            categories: data.quarter_name
	        }],
	        yAxis: [{ // Primary yAxis
	            labels: {
	                format: '{value}仟元',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            },
	            title: {
	                text: '營業收入',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            }
	        }, { // Secondary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '應收帳款週轉率',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            labels: {
	                format: '{value}',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            min: 0,	            
	            opposite: true
	        }, { // Tertiary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '存貨週轉率',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            labels: {
	                format: '{value}',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            min: 0,	            
	            opposite: true
	        }, { // more Tertiary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '存貨營收比',
	                style: {
	                    color: Highcharts.getOptions().colors[3]
	                }
	            },
	            labels: {
	                format: '{value}',
	                style: {
	                    color: Highcharts.getOptions().colors[3]
	                }
	            },
	            min: 0,	            
	            opposite: true
	        }],
	        tooltip: {
	            shared: true,
	            followPointer: true,
	            crosshairs: [{
                width: 2,
                color: 'yellow',
                dashStyle: 'shortdot'
            }, {
                width: 2,
                color: 'yellow',
                dashStyle: 'shortdot'
            }]
	        },
	        legend: {
	            align: 'center',
	            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
	        },
	        series: [{
	            name: '營業收入',
	            type: 'column',
	            yAxis: 0,
	            data: data.total_operating_revenue,
	            tooltip: {
	                valueSuffix: ' 仟元'
	            }

	        }, {
	            name: '應收帳款週轉率',
	            type: 'spline',
	            yAxis: 1,
	            data: data.accounts_receivable_turnover_ratio,
	            marker: {
	                enabled: true
	            },	            
	            tooltip: {
	                valueSuffix: ' 次/年'
	            },
	            dataLabels: {
                    align: 'right',
                    color: 'yellow',
                    enabled: true
                },
	            zIndex: 5
	        }, {
	            name: '存貨週轉率',
	            type: 'spline',
	            yAxis: 2,
	            data: data.inventory_turnover_ratio,
	            marker: {
	                enabled: true
	            },	            
	            tooltip: {
	                valueSuffix: ' 次/年'
	            },
	            dashStyle: 'shortdot'
	        }, {
	            name: '存貨營收比',
	            type: 'spline',
	            yAxis: 3,
	            data: data.inventory_sales_ratio,
	            marker: {
	                enabled: true
	            },
	            // dashStyle: 'shortdot',
	            tooltip: {
	                valueSuffix: ' 季'
	            },
	            dashStyle: 'shortdot'
	        }]
	    });
		// HighChart程式碼結束位置
    });
};

function potentialrisk_indicator() {
    $.getJSON("/potentialrisk_indicator/", function (data) {
        // 載入Highchart Dark-unica theme
        Highcharts.setOptions(Highcharts.theme);
        // 貼上HighChart的程式碼
        $('.container#chart').highcharts({
	        chart: {
	            zoomType: 'xy'
	        },
	        title: {
	            text: '金融負債比率/潛在風險指標'
	        },
	        subtitle: {
	            text: 'Source: 公開資訊觀測站'
	        },
	        xAxis: [{
	            categories: data.quarter_name
	        }],
	        yAxis: [{ // Primary yAxis
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            title: {
	                text: '金融負債比率',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            min: 0
	        }, { // Secondary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '無形資產比率',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            opposite: true,
	            min: 0
	        }, { // Tertiary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '備供出售比率',
	                style: {
	                    color: Highcharts.getOptions().colors[0]
	                }
	            },
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[0]
	                }
	            },
	            opposite: true,
	            min: 0
	        }],
	        tooltip: {
	            shared: true,
	            followPointer: true,
	            crosshairs: [{
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }, {
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }]
	        },
	        legend: {
	            align: 'center',
	            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
	        },
	        series: [{
	            name: '備供出售比率',
	            type: 'column',
	            yAxis: 2,
	            data: data.available_for_sale_to_equity_ratio,
	            tooltip: {
	                valueSuffix: ' %'
	            }
	        }, {
	            name: '無形資產比率',
	            type: 'column',
	            yAxis: 1,
	            data: data.intangible_asset_to_equity_ratio,
	            marker: {
	                enabled: true
	            },	            
	            tooltip: {
	                valueSuffix: ' %'
	            }
	        }, {
	            name: '金融負債比率',
	            type: 'spline',
	            yAxis: 0,
	            data: data.financial_debt_ratio,
	            marker: {
	                enabled: true
	            },
	            tooltip: {
	                valueSuffix: ' %'
	            },
	            dataLabels: {
                    align: 'right',
                    color: 'yellow',
                    enabled: true
                },
	            zIndex: 5
	        }]
	    });
		// HighChart程式碼結束位置
    });
};

function profitable_indicator_1() {
    $.getJSON("/profitable_indicator_1/", function (data) {
        // 載入Highchart Dark-unica theme
        Highcharts.setOptions(Highcharts.theme);
        // 貼上HighChart的程式碼
        $('.container#chart').highcharts({
	        chart: {
	            alignThresholds: true,
	            zoomType: 'xy'
	        },
	        title: {
	            text: '營益率/獲利性指標1 vs 營收年增率'
	        },
	        subtitle: {
	            text: 'Source: 公開資訊觀測站'
	        },
	        xAxis: [{
	            categories: data.quarter_name
	        }],
	        yAxis: [{ // Primary yAxis
	            labels: {
	                format: '{value}元',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            },
	            title: {
	                text: '每股盈餘EPS',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            }
	        }, { // Secondary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '營益率',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            opposite: true
	        }, { // Tertiary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '營收年增率',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            opposite: true
	        }],
	        tooltip: {
	            shared: true,
	            followPointer: true,
	            crosshairs: [{
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }, {
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }]
	        },
	        legend: {
	            align: 'center',
	            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
	        },
	        series: [{
	            name: '每股盈餘EPS',
	            type: 'column',
	            yAxis: 0,
	            data: data.earnings_per_share,
	            tooltip: {
	                valueSuffix: ' 元'
	            }
	        }, {
	            name: '營益率',
	            type: 'spline',
	            yAxis: 1,
	            data: data.operating_profit_margin,
	            marker: {
	                enabled: true
	            },
	            dataLabels: {
                    align: 'right',
                    color: 'yellow',
                    enabled: true
                },tooltip: {
	                valueSuffix: ' %'
	            },
	            zIndex: 5
	        }, {
	            name: '營收年增率',
	            type: 'column',
	            yAxis: 2,
	            data: data.total_operating_revenue_yoy,
	            marker: {
	                enabled: true
	            },
	            tooltip: {
	                valueSuffix: ' %'
	            }
	        }]
	    });
		// HighChart程式碼結束位置
    });
};

function profitable_indicator_2() {
    $.getJSON("/profitable_indicator_2/", function (data) {
        // 載入Highchart Dark-unica theme
        Highcharts.setOptions(Highcharts.theme);
        // 貼上HighChart的程式碼
        $('.container#chart').highcharts({
	        chart: {
	            zoomType: 'xy'
	        },
	        title: {
	            text: '毛利率/獲利性指標2 vs 每股盈餘'
	        },
	        subtitle: {
	            text: 'Source: 公開資訊觀測站'
	        },
	        xAxis: [{
	            categories: data.quarter_name
	        }],
	        yAxis: [{ // Primary yAxis
	            labels: {
	                format: '{value}元',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            },
	            title: {
	                text: '每股盈餘EPS',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            }
	        }, { // Secondary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '毛利率',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            opposite: true
	        }, { // Tertiary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '折舊負擔比率',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },	            
	            opposite: true
	        }],
	        tooltip: {
	            shared: true,
	            followPointer: true,
	            crosshairs: [{
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }, {
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }]
	        },
	        legend: {
	            align: 'center',
	            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
	        },
	        series: [{
	            name: '每股盈餘EPS',
	            type: 'column',
	            yAxis: 0,
	            data: data.earnings_per_share,
	            tooltip: {
	                valueSuffix: ' 元'
	            }
	        }, {
	            name: '毛利率',
	            type: 'spline',
	            yAxis: 1,
	            data: data.gross_profit_margin,
	            marker: {
	                enabled: true
	            },
	            // dashStyle: 'shortdot',
	            tooltip: {
	                valueSuffix: ' %'
	            },
	            dataLabels: {
                    align: 'right',
                    color: 'yellow',
                    enabled: true
                },
	            zIndex: 5
	        }, {
	            name: '折舊負擔比率',
	            type: 'spline',
	            yAxis: 2,
	            data: data.depreciation_to_sales_ratio,
	            marker: {
	                enabled: true
	            },
	            dashStyle: 'shortdot',
	            tooltip: {
	                valueSuffix: ' %'
	            }

	        }]
	    });
		// HighChart程式碼結束位置
    });
};

function stability_indicator() {
    $.getJSON("/stability_indicator/", function (data) {
        // 載入Highchart Dark-unica theme
        Highcharts.setOptions(Highcharts.theme);
        // 貼上HighChart的程式碼
        $('.container#chart').highcharts({
	        chart: {
	            zoomType: 'xy'
	        },
	        title: {
	            text: '本業獲利比重 vs 每股盈餘'
	        },
	        subtitle: {
	            text: 'Source: 公開資訊觀測站'
	        },
	        xAxis: [{
	            categories: data.quarter_name
	        }],
	        yAxis: [{ // Primary yAxis
	            labels: {
	                format: '{value}仟元',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            },
	            title: {
	                text: '營業利益',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            }
	        }, { // Secondary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '本業獲利比重',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            opposite: true
	        }, { // Tertiary yAxis
	            gridLineWidth: 0,
	            title: {
	                text: '每股盈餘EPS',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            labels: {
	                format: '{value}元',
	                style: {
	                    color: Highcharts.getOptions().colors[2]
	                }
	            },
	            opposite: true
	        }],
	        tooltip: {
	            shared: true,
	            followPointer: true,
	            crosshairs: [{
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }, {
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }]
	        },
	        legend: {
	            align: 'center',
	            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
	        },
	        series: [{
	            name: '營業利益',
	            type: 'column',
	            yAxis: 0,
	            data: data.net_operating_income_loss,
	            tooltip: {
	                valueSuffix: ' 仟元'
	            }
	        }, {
	            name: '本業獲利比重',
	            type: 'spline',
	            yAxis: 1,
	            data: data.operating_profit_to_net_profit_before_tax_ratio,
	            marker: {
	                enabled: true
	            },	            
	            tooltip: {
	                valueSuffix: ' %'
	            },
	            dataLabels: {
                    align: 'right',
                    color: 'yellow',
                    enabled: true
                },
	            zIndex: 5
	        }, {
	            name: '每股盈餘EPS',
	            type: 'column',
	            yAxis: 2,
	            data: data.earnings_per_share,
	            tooltip: {
	                valueSuffix: ' 元'
	            }
	        }]
	    });
		// HighChart程式碼結束位置
    });
};

function cashflow_indicator() {
    $.getJSON("/cashflow_indicator/", function (data) {
        // 載入Highchart Dark-unica theme
        Highcharts.setOptions(Highcharts.theme);
        // 貼上HighChart的程式碼
        $('.container#chart').highcharts({
	        chart: {
	            zoomType: 'xy'
	        },
	        title: {
	            text: '自由現金流量 vs 營業利益'
	        },
	        subtitle: {
	            text: 'Source: 公開資訊觀測站'
	        },
	        xAxis: [{
	            categories: data.quarter_name
	        }],
	        yAxis: [{ // Primary yAxis
	            labels: {
	                format: '{value}仟元',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            },
	            title: {
	                text: '營業利益 / 現金流量',
	                style: {
	                    color: Highcharts.getOptions().colors[10]
	                }
	            }
	        }],
	        tooltip: {
	            shared: true,
	            followPointer: true,
	            crosshairs: [{
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }, {
                width: 1,
                color: 'yellow',
                dashStyle: 'shortdot'
            }]
	        },
	        legend: {
	            align: 'center',
	            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
	        },
	        series: [{
	            name: '營業利益',
	            type: 'column',
	            yAxis: 0,
	            data: data.net_operating_income_loss,
	            tooltip: {
	                valueSuffix: ' 仟元'
	            }
	        }, {
	            name: '營業現金流量',
	            type: 'column',
	            yAxis: 0,
	            data: data.net_cash_flows_from_used_in_operating_activities,
	            tooltip: {
	                valueSuffix: ' 仟元'
	            }
	        }, {
	            name: '自由現金流量',
	            type: 'area',
	            yAxis: 0,
	            data: data.free_cash_flow,
	            tooltip: {
	                valueSuffix: ' 仟元'
	            },
	            dataLabels: {
                    align: 'right',
                    color: 'yellow',
                    enabled: true,
                    verticalAlign: 'bottom'
                },
	            fillOpacity: 0.3,
	            zIndex: 5
	        }]
	    });
		// HighChart程式碼結束位置
    });
};