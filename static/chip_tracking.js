$(document).ready(function() {
	bigchip_tracking();
	bigchip_tracking_chart();
	$("li#bigchip_tracking").click(function() {
		bigchip_tracking_chart();
	});
});

//將數字轉成帶有千分位符號的格式
function number_format(n) {
	 n += "";
	 var arr = n.split(".");
	 var re = /(\d{1,3})(?=(\d{3})+$)/g;
	 return arr[0].replace(re,"$1,") + (arr.length == 2 ? "."+arr[1] : "");
};

function bigchip_tracking() {
	$.ajax({
		url:"/bigchip_tracking/",
		type: "GET",
		dataType: "json",
		success: function(data) {
			// 先將股價資料按照日期填入表格(較新的資料在上)
			console.log(data);
			var i = data.stock_date.length-1;
			$.each(data.stock_date, function() {
				$("#price_chip_data").append(
					// 日期
					"<tr><td style='text-align:center'>" + data.stock_date[i] + "</td>" +
					// 開盤價
					"<td style='text-align:center'>" + data.stock_open[i] + "</td>" +
					// 最高價
					"<td style='text-align:center'>" + data.stock_high[i] + "</td>" +
					// 最低價
					"<td style='text-align:center'>" + data.stock_low[i] + "</td>" +
					// 收盤價
					"<td style='text-align:center'>" + data.stock_close[i] + "</td>" +
					// 大戶人數(1,000張以上)
					"<td style='text-align:center'>" + number_format(data.bigchip_holders[i]) + "</td>" +
					// 持有張數
					"<td style='text-align:center'>" + number_format(data.bigchip_holdings[i]) + "</td>" +
					// 持有比率
					"<td style='text-align:center'>" + data.bigchip_percent[i] + "</td>" +
					// 張數增減
					"<td style='text-align:center'>" + number_format(data.bigchip_monthly_change[i]) + "</td>" +
					// 大戶人數(800~1,000張)
					"<td style='text-align:center'>" + number_format(data.bigchip_holders_2nd[i]) + "</td>" +
					// 持有張數
					"<td style='text-align:center'>" + number_format(data.bigchip_holdings_2nd[i]) + "</td>" +
					// 持有比率
					"<td style='text-align:center'>" + data.bigchip_percent_2nd[i] + "</td>" +
					// 大戶人數(600~800張)
					"<td style='text-align:center'>" + number_format(data.bigchip_holders_3rd[i]) + "</td>" +
					// 持有張數
					"<td style='text-align:center'>" + number_format(data.bigchip_holdings_3rd[i]) + "</td>" +
					// 持有比率
					"<td style='text-align:center'>" + data.bigchip_percent_3rd[i] + "</td>"+
					// 大戶人數(小計)
					"<td style='text-align:center'>" + number_format(data.bigchip_holders[i]+data.bigchip_holders_2nd[i]+data.bigchip_holders_3rd[i]) + "</td>" +
					// 持有張數
					"<td style='text-align:center'>" + number_format(data.bigchip_holdings[i]+data.bigchip_holdings_2nd[i]+data.bigchip_holdings_3rd[i]) + "</td>" +
					// 持有比率
					"<td style='text-align:center'>" + parseFloat(data.bigchip_percent[i]+data.bigchip_percent_2nd[i]+data.bigchip_percent_3rd[i]).toPrecision(4) + "</td></tr>"

				);
				i--;
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
	colors: ["#7798BF", "#2b908f", "#90ee7e", "#f45b5b", "#7798BF", "#aaeeee", "#ff0066", "#eeaaee",
		"#55BF3B", "#DF5353", "#aaeeee"],
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

function bigchip_tracking_chart() {
    $.getJSON("/bigchip_tracking_chart/", function (data) {
        // 載入Highchart Dark-unica theme
        Highcharts.setOptions(Highcharts.theme);
        // 貼上HighChart的程式碼
        // split the data set into ohlc and volume
		var ohlc = [],
			chips = [],
			dataLength = data.stock_date.length;

		for (i = 0; i < dataLength; i++) {
			ohlc.push([
				data.stock_date[i], // the date
				data.stock_open[i], // open
				data.stock_high[i], // high
				data.stock_low[i], // low
				data.stock_close[i] // close
			]);			
			chips.push([
				data.stock_date[i], // the date
				data.bigchip_monthly_change[i] // the chips changed
			]);
		};
		// create the chart
		$('.container#chart').highcharts('StockChart', {
			credits: {
				enabled: false
			},
			navigator: {
				enabled: false
			},
			rangeSelector: {
				enabled: false
			},
			scrollbar: {
				enabled: false
			},
			plotOptions: {
				candlestick: {
					color: 'green',
					upColor: 'red',
					lineColor: 'white',
					upLineColor: 'white'
				}
			},
			title: {
				text: '標的股價走勢 vs 大戶籌碼增減'
			},
			subtitle: {
				text: 'Source: 台灣集中保管結算所, Yahoo Finance'
			},
			xAxis: {
				labels: {
					enabled: false
				},
				tickLength: 5,
				tickInterval: 1,
				tickPosition: 'inside',
				minRange: 30 * 24 * 3600 * 65
			},
			yAxis: [{
				title: {
					text: null
				},
				labels: {
					align: 'left',
					x: 10,
					format: '{value} 元',
					style: {
						color: 'white'
					}
				},
				height: '65%',
				lineWidth: 2,
				floor: 0,
				// gridLineDashStyle: 'shortdot',
				tickLength: 5,
				minTickInterval: 10,
				minorTickInterval: 'auto',
				minorGridLineDashStyle: 'shortdash',
				showFirstLabel: false,
				showLastLabel: true
			}, {
				title: {
					text: null
				},
				labels: {
					align: 'left',
					x: 10,
					format: '{value} 張',
					style: {
						color: 'white'
					}
				},
				top: '70%',
				height: '30%',
				lineWidth: 2,
				tickLength: 5,
				minorTickInterval: 'auto',
				minorGridLineDashStyle: 'shortdash',
				showLastLabel: true,
				offset: 0
			}],
			tooltip: {
				shared: true,
            followPointer: true,
            crosshairs: {
                width: 2,
                color: 'gray',
                dashStyle: 'shortdot'
            }
			},
			series: [{
				type: 'candlestick',
				name: data.symbol + "(" + data.cname + ")",
				data: ohlc,
				dataGrouping: {
					enabled: false
				},
				tooltip: {
					valueSuffix: ' 元'
				},
			}, {
				type: 'column',
				name: '增減',
				data: chips,
				yAxis: 1,
				// dataLabels: {
				// 	align: 'center',
				// 	color: '#DFDFDF',
				// 	enabled: true
				// },
				tooltip: {
					valueSuffix: ' 張'
				},
            borderWidth: 1
         }]
		});
		// HighChart程式碼結束位置
	});
};