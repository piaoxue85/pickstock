$(document).ready(function() {
	tw_economics();
	tw_economics_leading();
	$("li#tw_economics_leading").click(function() {
		tw_economics_leading();
	});
	$("li#tw_economics_pbr").click(function() {
		tw_economics_pbr();
	});
	$("li#tw_economics_m1b").click(function() {
		tw_economics_m1b();
	});
});

//將數字轉成帶有千分位符號的格式
function number_format(n) {
	n += "";
	var arr = n.split(".");
	var re = /(\d{1,3})(?=(\d{3})+$)/g;
	return arr[0].replace(re,"$1,") + (arr.length == 2 ? "."+arr[1] : "");
};

function tw_economics() {
	$.ajax({
		url:"/tw_economics/",
		type: "GET",
		dataType: "json",
		success: function(data) {
			console.log(data);
			// 將資料按照日期填入表格(較新的資料在上)
			var i = data.twse_date.length-1;
			$.each(data.twse_date, function() {
				$("#tw_economics_data").append("<tr>" +
					"<td style='text-align:center'>" + data.twse_date[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_open[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_high[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_low[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_close[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_pbr[i].toFixed(2) + "</td>" +
					"<td style='text-align:center'>" + data.twse_pbr10[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_pbr13[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_pbr16[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_pbr19[i] + "</td>" +
					"<td style='text-align:center'>" + data.twse_pbr22[i] + "</td>" +
					"<td style='text-align:center'>" + data.monitoring_indicator[i] + "</td>" +
					"<td style='text-align:center'>" + data.composite_leading_index[i] + "</td>" +
					"<td style='text-align:center'>" + data.composite_leading_index_yoy[i] + "</td>" +
					"<td style='text-align:center'>" + number_format(data.monetary_aggregates_M1B[i]) + "</td>" +
					"<td style='text-align:center'>" + data.monetary_aggregates_M1B_yoy[i] + "</td>" +
					"</tr>"
				);
				i--;
			});
		},
		error: function() {
			alert("ERROR!!!");
		}
	});
};

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

function tw_economics_leading() {
	$.getJSON("/tw_economics/", function (data) {
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		// split the data set into ohlc and 景氣指標
		var ohlc = [],
			leading = [],
			dataLength = data.twse_date.length;

		for (i = 0; i < dataLength; i++) {
			ohlc.push([
				data.twse_date[i], // the date
				data.twse_open[i], // open
				data.twse_high[i], // high
				data.twse_low[i], // low
				data.twse_close[i] // close
			]);
			// 景氣指標
			leading.push([
				data.twse_date[i], // the date
				data.composite_leading_index_yoy[i] // 領先指標年增率
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
				text: '加權指數河流圖 vs 領先指標年增率'
			},
			subtitle: {
				text: 'Source: Yahoo Finance, 國家發展委員會'
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
				// 上方的圖
				title: {
					text: null
				},
				labels: {
					align: 'left',
					x: 10,
					format: '{value} 點',
					style: {
						color: 'white'
					}
				},
				height: '70%',
				lineWidth: 2,
				floor: 3000,
				ceiling: 11000,
				tickLength: 5,
				tickInterval:2000,
				minTickInterval: 1000,
				minorTickInterval: 1000,
				minorGridLineDashStyle: 'shortdash',
				showFirstLabel: true,
				showLastLabel: true
			}, {
				// 下方的圖
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
				top: '74%',
				height: '26%',
				max: 40,
				min: -20,
				lineWidth: 2,
				tickLength: 5,
				tickInterval:20,
				gridLineDashStyle: 'shortdash',
				showLastLabel: true,
				offset: 0,
				// 加入區間帶的說明
				plotLines: [{ // mark the level
					color: 'red',
					width: 2,
					value: 0,
					dashStyle: 'shortdash',
					zIndex: 5,
					label: {
						text: '每當YoY轉負值後，指數都出現急挫，等YoY落底收斂時，是最好的佈局時機',
						align: 'right',
						x: -10,
						y: 20,
						style: {
							color: 'yellow',
							fontWeight: 'bold'
						}
					}
				}],
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
				name: "加權指數",
				id: "primary",
				data: ohlc,
				dataGrouping: {
					enabled: false
				},
				zIndex: 1
			}, {
				type: 'spline',
				name: '1.0x',
				data: data.twse_pbr10,
				id: 'pbr10',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#00FFFF'
			}, {
				type: 'spline',
				name: '1.3x',
				data: data.twse_pbr13,
				id: 'pbr13',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: 'lightgreen'
			}, {
				type: 'spline',
				name: '1.6x',
				data: data.twse_pbr16,
				id: 'pbr16',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#E3E2DD'
			}, {
				type: 'spline',
				name: '1.9x',
				data: data.twse_pbr19,
				id: 'pbr19',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#FFC04C'
			}, {
				type: 'spline',
				name: '2.2x',
				data: data.twse_pbr22,
				id: 'pbr22',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: 'red'
			}, {
				type: 'column',
				name: '領先指標年增率',
				data: leading,
				yAxis: 1,
				tooltip: {
					valueSuffix: '%'
				},
				borderWidth: 1
			}, {
				type: 'flags',
				data: [{
					x : 5,
					title: '持股90%'
				}],
				onSeries: 'pbr10',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 5,
					title: '持股70%'
				}],
				onSeries: 'pbr13',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 52,
					title: '持股50%'
				}],
				onSeries: 'pbr16',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 115,
					title: '持股30%'
				}],
				onSeries: 'pbr19',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 115,
					title: '持股10%'
				}],
				onSeries: 'pbr22',
				shape : 'squarepin'
			}]
		});
		// HighChart程式碼結束位置
	});
};

function tw_economics_pbr() {
	$.getJSON("/tw_economics/", function (data) {
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		// split the data set into ohlc and 景氣指標
		var ohlc = [],
			pbr = [],
			dataLength = data.twse_date.length;

		for (i = 0; i < dataLength; i++) {
			ohlc.push([
				data.twse_date[i], // the date
				data.twse_open[i], // open
				data.twse_high[i], // high
				data.twse_low[i], // low
				data.twse_close[i] // close
			]);
			// 景氣指標
			pbr.push([
				data.twse_date[i], // the date
				data.monitoring_indicator[i] // 景氣對策信號分數
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
				text: '加權指數河流圖 vs 景氣對策信號分數'
			},
			subtitle: {
				text: 'Source: Yahoo Finance, 證交所'
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
				// 上方的圖
				title: {
					text: null
				},
				labels: {
					align: 'left',
					x: 10,
					format: '{value} 點',
					style: {
						color: 'white'
					}
				},
				height: '70%',
				lineWidth: 2,
				floor: 3000,
				ceiling: 11000,
				tickLength: 5,
				tickInterval:2000,
				minTickInterval: 1000,
				minorTickInterval: 1000,
				minorGridLineDashStyle: 'shortdash',
				showFirstLabel: true,
				showLastLabel: true
			}, {
				// 下方的圖
				title: {
					text: null
				},
				labels: {
					align: 'left',
					x: 10,
					format: '{value} 分',
					style: {
						color: 'white'
					}
				},
				top: '74%',
				height: '26%',
				max: 40,
				min: 0,
				lineWidth: 2,
				tickLength: 5,
				tickInterval:10,
				gridLineDashStyle: 'shortdash',
				// minorTickInterval: '5',
				// minorGridLineDashStyle: 'shortdash',
				showLastLabel: true,
				offset: 0,
				// 加入區間帶的說明
				plotLines: [{ // mark the level
					color: 'red',
					width: 2,
					value: 17,
					dashStyle: 'shortdash',
					zIndex: 5,
					label: {
						text: '17分以下增加持股',
						align: 'right',
						x: -10,
						y: 20,
						style: {
							color: 'yellow',
							fontWeight: 'bold'
						}
					}
				},{ // mark the level
					color: 'red',
					width: 2,
					value: 29,
					dashStyle: 'shortdash',
					zIndex: 5,
					label: {
						text: '29分以上出脫持股',
						align: 'right',
						x: -10,
						y: -10,
						style: {
							color: 'yellow',
							fontWeight: 'bold'
						}
					}
				}],
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
				name: "加權指數",
				id: "primary",
				data: ohlc,
				dataGrouping: {
					enabled: false
				},
				zIndex: 1
			}, {
				type: 'spline',
				name: '1.0x',
				data: data.twse_pbr10,
				id: 'pbr10',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#00FFFF'
			}, {
				type: 'spline',
				name: '1.3x',
				data: data.twse_pbr13,
				id: 'pbr13',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: 'lightgreen'
			}, {
				type: 'spline',
				name: '1.6x',
				data: data.twse_pbr16,
				id: 'pbr16',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#E3E2DD'
			}, {
				type: 'spline',
				name: '1.9x',
				data: data.twse_pbr19,
				id: 'pbr19',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#FFC04C'
			}, {
				type: 'spline',
				name: '2.2x',
				data: data.twse_pbr22,
				id: 'pbr22',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: 'red'
			}, {
				type: 'column',
				name: '景氣對策信號',
				data: pbr,
				yAxis: 1,
				tooltip: {
					valueSuffix: '分'
				},
				borderWidth: 1
			}, {
				type: 'flags',
				data: [{
					x : 5,
					title: '持股90%'
				}],
				onSeries: 'pbr10',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 5,
					title: '持股70%'
				}],
				onSeries: 'pbr13',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 52,
					title: '持股50%'
				}],
				onSeries: 'pbr16',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 115,
					title: '持股30%'
				}],
				onSeries: 'pbr19',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 115,
					title: '持股10%'
				}],
				onSeries: 'pbr22',
				shape : 'squarepin'
			}]
		});
		// HighChart程式碼結束位置
	});
};

function tw_economics_m1b() {
	$.getJSON("/tw_economics/", function (data) {
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		// split the data set into ohlc and 景氣指標
		var ohlc = [],
			m1b = [],
			dataLength = data.twse_date.length;

		for (i = 0; i < dataLength; i++) {
			ohlc.push([
				data.twse_date[i], // the date
				data.twse_open[i], // open
				data.twse_high[i], // high
				data.twse_low[i], // low
				data.twse_close[i] // close
			]);
			// 景氣指標
			m1b.push([
				data.twse_date[i], // the date
				data.monetary_aggregates_M1B_yoy[i] // 貨幣總額M1B年增率
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
				text: '加權指數河流圖 vs 貨幣總額M1B年增率'
			},
			subtitle: {
				text: 'Source: Yahoo Finance, 國家發展委員會'
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
				// 上方的圖
				title: {
					text: null
				},
				labels: {
					align: 'left',
					x: 10,
					format: '{value} 點',
					style: {
						color: 'white'
					}
				},
				height: '70%',
				lineWidth: 2,
				floor: 3000,
				ceiling: 11000,
				tickLength: 5,
				tickInterval:2000,
				minTickInterval: 1000,
				minorTickInterval: 1000,
				minorGridLineDashStyle: 'shortdash',
				showFirstLabel: true,
				showLastLabel: true
			}, {
				// 下方的圖
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
				top: '74%',
				height: '26%',
				max: 40,
				min: -10,
				lineWidth: 2,
				tickLength: 5,
				tickInterval:10,
				gridLineDashStyle: 'shortdash',
				showLastLabel: true,
				offset: 0,
				// 加入區間帶的說明
				plotLines: [{ // mark the level
					color: 'red',
					width: 2,
					value: 0,
					dashStyle: 'shortdash',
					zIndex: 5,
					label: {
						text: 'YoY由負轉正時，通常是最好的佈局時機',
						align: 'right',
						x: -10,
						y: 20,
						style: {
							color: 'yellow',
							fontWeight: 'bold'
						}
					}
				}],
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
				name: "加權指數",
				id: "primary",
				data: ohlc,
				dataGrouping: {
					enabled: false
				},
				zIndex: 1
			}, {
				type: 'spline',
				name: '1.0x',
				data: data.twse_pbr10,
				id: 'pbr10',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#00FFFF'
			}, {
				type: 'spline',
				name: '1.3x',
				data: data.twse_pbr13,
				id: 'pbr13',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: 'lightgreen'
			}, {
				type: 'spline',
				name: '1.6x',
				data: data.twse_pbr16,
				id: 'pbr16',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#E3E2DD'
			}, {
				type: 'spline',
				name: '1.9x',
				data: data.twse_pbr19,
				id: 'pbr19',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: '#FFC04C'
			}, {
				type: 'spline',
				name: '2.2x',
				data: data.twse_pbr22,
				id: 'pbr22',
				linkedTo: 'primary',
				lineWidth: 2,
				dashStyle: 'shortdot',
				color: 'red'
			}, {
				type: 'column',
				name: 'M1B年增率',
				data: m1b,
				yAxis: 1,
				tooltip: {
					valueSuffix: '%'
				},
				borderWidth: 1
			}, {
				type: 'flags',
				data: [{
					x : 5,
					title: '持股90%'
				}],
				onSeries: 'pbr10',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 5,
					title: '持股70%'
				}],
				onSeries: 'pbr13',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 52,
					title: '持股50%'
				}],
				onSeries: 'pbr16',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 115,
					title: '持股30%'
				}],
				onSeries: 'pbr19',
				shape : 'squarepin'
			}, {
				type: 'flags',
				data: [{
					x : 115,
					title: '持股10%'
				}],
				onSeries: 'pbr22',
				shape : 'squarepin'
			}]
		});
		// HighChart程式碼結束位置
	});
};