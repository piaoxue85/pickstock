$(document).ready(function() {
	sales_overview();
	season_effect();
	$("li#season_effect").click(function() {
		season_effect();
	});
	$("li#price_momentum_1").click(function() {
		price_momentum_1();    
	});
	$("li#price_momentum_2").click(function() {
		price_momentum_2();
	});
});

//將數字轉成帶有千分位符號的格式
function number_format(n) {
	n += "";
	var arr = n.split(".");
	var re = /(\d{1,3})(?=(\d{3})+$)/g;
	return arr[0].replace(re,"$1,") + (arr.length == 2 ? "."+arr[1] : "");
};

function sales_overview() {
	$.ajax({
		url:"/sales_overview/",
		type: "GET",
		dataType: "json",
		success: function(data) {          
			// 填入月份
			var i = 0;
			$.each(data.month_series, function() {
				$("#month_series").append(
					"<th style='text-align:center'>" + data.month_series[i] + "</th>"
				);
				i++;
			});
			// 填入年份
			var i = 0;
			$.each(data.year_series, function() {
				$("#sales_yr"+i).append(
					"<td rowspan=4 style='text-align:center'>" + data.year_series[i] + "</td>" +
					"<td style='text-align:center'>營收(仟元)</td>"
				);
				$("#sales_yoy_yr"+i).append(
					"<td style='text-align:center'>年增率(%)</td>"
				);
				$("#acc_sales_yr"+i).append(
					"<td style='text-align:center'>累積營收(仟元)</td>"
				);
				$("#acc_sales_yoy_yr"+i).append(
					"<td style='text-align:center'>年增率(%)</td>"
				);
				i++;
			});
			// 填入第1年
			var i = 0;
			$.each(data.sales_yr0, function() {
				$("#sales_yr0").append(
					"<td style='text-align:center'>" + number_format(data.sales_yr0[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.sales_yoy_yr0, function() {
				$("#sales_yoy_yr0").append(
					"<td style='text-align:center'>" + data.sales_yoy_yr0[i] + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yr0, function() {
				$("#acc_sales_yr0").append(
					"<td style='text-align:center'>" + number_format(data.acc_sales_yr0[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yoy_yr0, function() {
				$("#acc_sales_yoy_yr0").append(
					"<td style='text-align:center'>" + data.acc_sales_yoy_yr0[i] + "</td>"
				);
				i++;
			});
			// 填入第2年
			var i = 0;
			$.each(data.sales_yr1, function() {
				$("#sales_yr1").append(
					"<td style='text-align:center'>" + number_format(data.sales_yr1[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.sales_yoy_yr1, function() {
				$("#sales_yoy_yr1").append(
					"<td style='text-align:center'>" + data.sales_yoy_yr1[i] + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yr1, function() {
				$("#acc_sales_yr1").append(
					"<td style='text-align:center'>" + number_format(data.acc_sales_yr1[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yoy_yr1, function() {
				$("#acc_sales_yoy_yr1").append(
					"<td style='text-align:center'>" + data.acc_sales_yoy_yr1[i] + "</td>"
				);
				i++;
			});
			// 填入第3年
			var i = 0;
			$.each(data.sales_yr2, function() {
				$("#sales_yr2").append(
					"<td style='text-align:center'>" + number_format(data.sales_yr2[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.sales_yoy_yr2, function() {
				$("#sales_yoy_yr2").append(
					"<td style='text-align:center'>" + data.sales_yoy_yr2[i] + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yr2, function() {
				$("#acc_sales_yr2").append(
					"<td style='text-align:center'>" + number_format(data.acc_sales_yr2[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yoy_yr2, function() {
				$("#acc_sales_yoy_yr2").append(
					"<td style='text-align:center'>" + data.acc_sales_yoy_yr2[i] + "</td>"
				);
				i++;
			});
			// 填入第4年
			var i = 0;
			$.each(data.sales_yr3, function() {
				$("#sales_yr3").append(
					"<td style='text-align:center'>" + number_format(data.sales_yr3[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.sales_yoy_yr3, function() {
				$("#sales_yoy_yr3").append(
					"<td style='text-align:center'>" + data.sales_yoy_yr3[i] + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yr3, function() {
				$("#acc_sales_yr3").append(
					"<td style='text-align:center'>" + number_format(data.acc_sales_yr3[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yoy_yr3, function() {
				$("#acc_sales_yoy_yr3").append(
					"<td style='text-align:center'>" + data.acc_sales_yoy_yr3[i] + "</td>"
				);
				i++;
			});
			// 填入第5年
			var i = 0;
			$.each(data.sales_yr4, function() {
				$("#sales_yr4").append(
					"<td style='text-align:center'>" + number_format(data.sales_yr4[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.sales_yoy_yr4, function() {
				$("#sales_yoy_yr4").append(
					"<td style='text-align:center'>" + data.sales_yoy_yr4[i] + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yr4, function() {
				$("#acc_sales_yr4").append(
					"<td style='text-align:center'>" + number_format(data.acc_sales_yr4[i]) + "</td>"
				);
				i++;
			});
			var i = 0;
			$.each(data.acc_sales_yoy_yr4, function() {
				$("#acc_sales_yoy_yr4").append(
					"<td style='text-align:center'>" + data.acc_sales_yoy_yr4[i] + "</td>"
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
 * 以下這部分是Highchart的plugin，可以把多個Y軸的0對準在同一水平，直接複製貼上即可使用(偶而還是會有不一致)
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

function season_effect() {
	$.getJSON("/season_effect/", function (data) {
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		$('.container#chart').highcharts({
			chart: {
				zoomType: 'xy'
			},
			title: {
				text: '營收季節效應'
			},
			subtitle: {
				text: 'Source: 公開資訊觀測站'
			},
			xAxis: [{
				categories: data.month_series
			}],
			yAxis: [{ // Primary yAxis
				labels: {
					format: '{value}仟元',
					style: {
						color: Highcharts.getOptions().colors[10]
					}
				},
				title: {
					text: '月營收',
					style: {
						color: Highcharts.getOptions().colors[10]
					}
				}
			}, { // Secondary yAxis
				gridLineWidth: 0,
				title: {
					text: '年增率',
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
			}],
			// 可以把jsonData中None的值也連接起來
			plotOptions: {
			  series: {
				connectNulls: true
			  }
			},
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
				name: data.year_series[0],
				type: 'column',
				yAxis: 0,
				data: data.sales_yr0,
				tooltip: {
					valueSuffix: ' 仟元'
				}
			}, {
				name: data.year_series[0]+"年增率",
				type: 'area',
				yAxis: 1,
				data: data.sales_yoy_yr0,
				tooltip: {
					valueSuffix: ' %'
				},
				dataLabels: {
					align: 'cneter',
					color: 'yellow',
					enabled: true,
					verticalAlign: 'bottom',
					format: '{y}%'
				},
				fillOpacity: 0.3,
				dashStyle: 'shortdot'
			}, {
				name: data.year_series[1],
				type: 'spline',
				yAxis: 0,
				data: data.sales_yr1,
				tooltip: {
					valueSuffix: ' 仟元'
				}
			}, {
				name: data.year_series[2],
				type: 'spline',
				yAxis: 0,
				data: data.sales_yr2,
				tooltip: {
					valueSuffix: ' 仟元'
				},
				dashStyle: 'shortdot'
			}, {
				name: data.year_series[3],
				type: 'spline',
				yAxis: 0,
				data: data.sales_yr3,
				tooltip: {
					valueSuffix: ' 仟元'
				},
				dashStyle: 'shortdot'
			}, {
				name: data.year_series[4],
				type: 'spline',
				yAxis: 0,
				data: data.sales_yr4,
				tooltip: {
					valueSuffix: ' 仟元'
				},
				dashStyle: 'shortdot'
			}]
		});
	});
};

function price_momentum_1() {
	$.getJSON("/price_momentum/", function (data) {
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		// split the data set into ohlc and 景氣指標
		var ohlc = [], yoy = [],
			dataLength = data.stock_date.length;
		for (i = 0; i < dataLength; i++) {
		  	ohlc.push([
				data.stock_date[i], // the date
				data.stock_open[i], // open
				data.stock_high[i], // high
				data.stock_low[i], // low
				data.stock_close[i] // close
		  	]);
		  	yoy.push([
				data.stock_date[i], // the date
				data.sales_yoy[i], // 營收年增率
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
				},
				series: {
					// 把jsonData中None的值也連接起來
					connectNulls: true
			  	}
		  	},
		  	title: {
				text: '股價月K線圖(上)、營收年增率(下)'
		  	},
		  	subtitle: {
				text: 'Source: 證交所, Yahoo Finance'
		  	},
		  	xAxis: {
				labels: {
			  		enabled: false
				},
				tickLength: 5,
				tickInterval: 1,
				tickPosition: 'inside'
		  	},
		  	yAxis: [{
				// 上方的圖, yAxis:0
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
				tickLength: 5,
				minorTickInterval: 'auto',
				minorGridLineDashStyle: 'shortdash',
				showFirstLabel: true,
				showLastLabel: true
		  	}, {
				// 下方的圖, yAxis:1
				title: {
			  		text: null
				},
				labels: {
			  		align: 'left',
			 		x: 10,
			  		format: '{value} %',
			  		style: {
						color: 'white'
			  		}
				},
				top: '70%',
				height: '30%',
				lineWidth: 2,
				tickLength: 5,
				gridLineDashStyle: 'shortdash',
				showLastLabel: true,
				offset: 0
		  	}],
		  	tooltip: {
				shared: true,
				followPointer: true,
				crosshairs: {
			  		width: 2,
			  		color: 'white',
			  		dashStyle: 'shortdot'
				}
		  	},
		  	series: [{
				type: 'candlestick',
				name: "月股價行情",				
				data: ohlc,
				dataGrouping: {
			  		enabled: false
				}
		  	}, {
				type: 'area',
				name: '年增率',
				data: yoy,
				tooltip: {
			  		valueSuffix: '%'
				},
				dataLabels: {
					align: 'cneter',
					color: 'yellow',
					enabled: true,
					verticalAlign: 'bottom',
					format: '{y}%'
				},
				fillOpacity: 0.3,
				dashStyle: 'shortdot',
				borderWidth: 1,
				yAxis:1	
		  	}]
		});
		// HighChart程式碼結束位置
  	});
};

function price_momentum_2() {
	$.getJSON("/price_momentum/", function (data) {
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		// split the data set into ohlc and 景氣指標
		var ohlc = [], acc_yoy = [],
			dataLength = data.stock_date.length;
		for (i = 0; i < dataLength; i++) {
		  	ohlc.push([
				data.stock_date[i], // the date
				data.stock_open[i], // open
				data.stock_high[i], // high
				data.stock_low[i], // low
				data.stock_close[i] // close
		  	]);
		  	acc_yoy.push([
				data.stock_date[i], // the date
				data.acc_sales_yoy[i], // 累積營收年增率
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
				},
				series: {
					// 把jsonData中None的值也連接起來
					connectNulls: true
			  	}
		  	},
		  	title: {
				text: '股價月K線圖(上)、累積營收年增率(下)'
		  	},
		  	subtitle: {
				text: 'Source: 證交所, Yahoo Finance'
		  	},
		  	xAxis: {
				labels: {
			  		enabled: false
				},
				tickLength: 5,
				tickInterval: 1,
				tickPosition: 'inside'
		  	},
		  	yAxis: [{
				// 上方的圖, yAxis:0
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
				tickLength: 5,
				minorTickInterval: 'auto',
				minorGridLineDashStyle: 'shortdash',
				showFirstLabel: true,
				showLastLabel: true
		  	}, {
				// 下方的圖, yAxis:1
				title: {
			  		text: null
				},
				labels: {
			  		align: 'left',
			 		x: 10,
			  		format: '{value} %',
			  		style: {
						color: 'white'
			  		}
				},
				top: '70%',
				height: '30%',
				lineWidth: 2,
				tickLength: 5,
				gridLineDashStyle: 'shortdash',
				showLastLabel: true,
				offset: 0
		  	}],
		  	tooltip: {
				shared: true,
				followPointer: true,
				crosshairs: {
			  		width: 2,
			  		color: 'white',
			  		dashStyle: 'shortdot'
				}
		  	},
		  	series: [{
				type: 'candlestick',
				name: "月股價行情",				
				data: ohlc,
				dataGrouping: {
			  		enabled: false
				}
		  	}, {
				type: 'area',
				name: '累積年增率',
				data: acc_yoy,
				tooltip: {
			  		valueSuffix: '%'
				},
				dataLabels: {
					align: 'cneter',
					color: 'yellow',
					enabled: true,
					verticalAlign: 'bottom',
					format: '{y}%'
				},				
				fillOpacity: 0.3,
				dashStyle: 'shortdot',
				borderWidth: 1,
				yAxis:1	
		  	}]
		});
		// HighChart程式碼結束位置
  	});
};





function sales_momentum_old() {
	$.getJSON("/sales_momentum/", function (data) {
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		$('.container#chart').highcharts({
			chart: {
				zoomType: 'xy'
			},
			title: {
				text: '營收成長趨勢'
			},
			subtitle: {
				text: 'Source: 公開資訊觀測站'
			},
			xAxis: [{
				categories: data.xAxis_cat_series,
				labels: {
					rotation: 0
				}
			}],
			yAxis: [{ // Primary yAxis
				labels: {
					format: '{value} 仟元'
				},
				title: {
					text: '月營收'
				}
			}, { // Secondary yAxis
				title: {
					text: '營收年增率'
				},
				labels: {
					format: '{value} %'
				},
				opposite: true
			}],
			tooltip: {
				shared: false,
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
				name: '月營收YoY',
				type: 'column',
				yAxis: 1,
				data: data.salesyoy_series,
				tooltip: {
					valueSuffix: ' %'
				},
				dataLabels: {
					align: 'right',
					color: 'yellow',
					enabled: true,
					verticalAlign: 'bottom',
				}
			}, {
				name: '累積月營收YoY',
				type: 'column',
				yAxis: 1,
				data: data.accsalesyoy_series,
				tooltip: {
					valueSuffix: ' %'
				},
				dataLabels: {
					align: 'left',
					color: 'white',
					enabled: true,
					verticalAlign: 'bottom',
				}                
			}, {
				name: '月營收',
				type: 'area',
				data: data.sales_series,
				tooltip: {
					valueSuffix: ' 仟元'
				},
				fillOpacity: 0.3,
				zIndex: 1
			}]
		});   
	});
};

// 舊的填表格方式，程式中已經沒有呼叫此函式
function fillTable(title, content) {
    var i, j, $cell;
    var max = 0;
    //先找出５年內營收數字最高的值
    for (i = 0; i < content.length; i++){
        for (j = 0; j < 11; j++){
            if (content[i][j] != undefined && content[i][j+1] != undefined){
                if (content[i][j] >= content[i][j+1]){
                    if (content[i][j] >= max){
                        max = content[i][j];
                    };                    
                } else{
                    if (content[i][j+1] >= max){
                        max = content[i][j+1];
                    };
                };
            };
        };
    };
    console.log(max);

    //根據最大值決定表頭的單位是百萬元還是仟元
    if (max >= 10000000){
        $("th#table_title").text("月營收(百萬元)");
    } else{
        $("th#table_title").text("月營收(仟元)");
    };

    //依序填入營收數字
    for (i = 0; i < content.length; i++){
        for (j = 0; j <= 12; j++){            
            $cell = $("td#year-" + (i+1) + "-" + j);
            if (j == 0) {
                $cell.text(title[i]);
            } else{
                if (max >= 10000000){
                    if (content[i][j-1] != undefined){
                        $cell.text(number_format((content[i][j-1]/1000).toFixed(0)));
                    };
                } else{
                    if (content[i][j-1] != undefined){
                        $cell.text(number_format((content[i][j-1]).toFixed(0)));
                    };
                };
            };
        };
    };
};