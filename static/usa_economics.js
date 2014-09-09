$(document).ready(function() {
	usa_economics_gdp_contribution();
	$("li#usa_economics_gdp_contribution").click(function() {
		usa_economics_gdp_contribution();
		$('.container#chart').show();
	});
	$("li#usa_economics_gdp").click(function() {
		usa_economics_gdp();
		$('.container#chart').show();
	});
	$("li#usa_economics_unrate").click(function() {
		usa_economics_unrate();
		$('.container#chart').show();
	});
	$("li#usa_economics_inflation").click(function() {
		usa_economics_inflation();
		$('.container#chart').show();
	});
	$("li#usa_economics_fxrate").click(function() {
		usa_economics_fxrate();
		$('.container#chart').show();
	});
});

// 將數字轉成帶有千分位符號的格式
function number_format(n) {
	n += "";
	var arr = n.split(".");
	var re = /(\d{1,3})(?=(\d{3})+$)/g;
	return arr[0].replace(re,"$1,") + (arr.length == 2 ? "."+arr[1] : "");
};
// --------------------------
//  *** GDP佔比分析 ***
// --------------------------
function usa_economics_gdp_contribution() {
	$("#usa_eco_footer").html("");
	$("#usa_eco_footer").html("美國GDP佔全球1/4強，且民間消費佔比高達70%，讓美國穩坐全球最大進口國，其景氣榮枯牽動全球市場，<br>&nbsp&nbsp&nbsp&nbsp因此必須掌握其經濟情勢變化，並提前判斷貨幣政策風向。");
	$.when($.ajax("/usa_economics_real_gdp_contribution/"),
			$.ajax("/usa_economics_real_pce_contribution/"),
			$.ajax("/usa_economics_real_pcdg_contribution/"),
			$.ajax("/usa_economics_real_gpdi_contribution/"),
			$.ajax("/usa_economics_real_prfi_contribution/"),
			$.ajax("/usa_economics_real_pnfi_contribution/"),
			$.ajax("/usa_economics_real_impgs_contribution/"),
			$.ajax("/usa_economics_real_expgs_contribution/"),
			$.ajax("/usa_economics_real_gce_contribution/"),
			$.ajax("/usa_economics_real_gdp_amount/"),
			$.ajax("/usa_economics_real_pce_amount/"),
			$.ajax("/usa_economics_real_pcdg_amount/"),
			$.ajax("/usa_economics_real_gpdi_amount/"),
			$.ajax("/usa_economics_real_prfi_amount/"),
			$.ajax("/usa_economics_real_pnfi_amount/"),
			$.ajax("/usa_economics_real_impgs_amount/"),
			$.ajax("/usa_economics_real_expgs_amount/"),
			$.ajax("/usa_economics_real_gce_amount/")
			).done(function(real_gdp_crtb, real_pce_crtb, real_pcdg_crtb, real_gpdi_crtb, real_prfi_crtb, real_pnfi_crtb, real_impgs_crtb, real_expgs_crtb, real_gce_crtb,
				real_gdp_amt, real_pce_amt, real_pcdg_amt, real_gpdi_amt, real_prfi_amt, real_pnfi_amt, real_impgs_amt, real_expgs_amt, real_gce_amt){
		// ------------------
		// 步驟一：填入表格資料
		// ------------------
		var real_gdp_crtb_data = real_gdp_crtb[0].observations;
		var real_pce_crtb_data = real_pce_crtb[0].observations;
		var real_pcdg_crtb_data = real_pcdg_crtb[0].observations;
		var real_gpdi_crtb_data = real_gpdi_crtb[0].observations;
		var real_prfi_crtb_data = real_prfi_crtb[0].observations;
		var real_pnfi_crtb_data = real_pnfi_crtb[0].observations;
		var real_impgs_crtb_data = real_impgs_crtb[0].observations;
		var real_expgs_crtb_data = real_expgs_crtb[0].observations;
		var real_gce_crtb_data = real_gce_crtb[0].observations;
		var real_gdp_amt_data = real_gdp_amt[0].observations;
		var real_pce_amt_data = real_pce_amt[0].observations;
		var real_pcdg_amt_data = real_pcdg_amt[0].observations;
		var real_gpdi_amt_data = real_gpdi_amt[0].observations;
		var real_prfi_amt_data = real_prfi_amt[0].observations;
		var real_pnfi_amt_data = real_pnfi_amt[0].observations;
		var real_impgs_amt_data = real_impgs_amt[0].observations;
		var real_expgs_amt_data = real_expgs_amt[0].observations;
		var real_gce_amt_data = real_gce_amt[0].observations;
		// 清空表格標題和內容
		$("#usa_economics_data_title").html("");
		$("#usa_economics_data").html("");
		// 填入表格標題（實質GDP成長率）
		$("#usa_economics_data_title").append("<tr class='info' id='gdp_title'>" +
			"<th style='text-align:center'>GDP(子)項目</th>" +
			"<th style='text-align:center' colspan=2>實質GDP</th></tr>" +
			"<tr id='gdp_title_2'><th style='text-align:center' class='info' >日期(每季)</th>" + 
			"<th class='info' style='text-align:center' width='75px'>金額(blns)</th>" +
			"<th class='warning' style='text-align:center' width='55px'>成長率</th>" +
			"</tr>");
		// 填入表格內容（實質GDP成長率）
		var i = real_gdp_crtb_data.length - 1;
		$.each(real_gdp_crtb_data, function() {
			$("#usa_economics_data").append("<tr id=" + real_gdp_crtb_data[i].date + ">" +
				"<td style='text-align:center'>" + real_gdp_crtb_data[i].date + "</td>" +
				"<td style='text-align:center'>" + number_format(parseInt(real_gdp_amt_data[i].value)) + "</td>" +
				"<td style='text-align:center'>" + parseFloat(real_gdp_crtb_data[i].value).toFixed(2) + "</td>" +
				"</tr>"
			);
			i--;
		});
		// 填入表格標題（民間消費）
		$("#gdp_title").append("<th style='text-align:center' colspan=4>【1】民間消費</th>");
		$("#gdp_title_2").append("<th class='warning' style='text-align:center' width='65px'>民間消費</th>");
		$("#gdp_title_2").append("<th class='info'  style='text-align:center' width='45px'>(%)</th>");
		// 填入表格內容（民間消費）
		var i = real_pce_crtb_data.length - 1;
		$.each(real_pce_crtb_data, function() {
			$("#"+real_pce_crtb_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_pce_crtb_data[i].value).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + (parseFloat(real_pce_amt_data[i].value)/parseFloat(real_gdp_amt_data[i].value)*100).toFixed(1) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間消費/耐久財）
		$("#gdp_title_2").append("<th class='warning' style='text-align:center' width='65px'>(耐久財)</th>");
		$("#gdp_title_2").append("<th class='info'  style='text-align:center' width='45px'>(%)</th>");
		// 填入表格內容（民間消費/耐久財）
		var i = real_pcdg_crtb_data.length - 1;
		$.each(real_pcdg_crtb_data, function() {
			$("#"+real_pcdg_crtb_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_pcdg_crtb_data[i].value).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + (parseFloat(real_pcdg_amt_data[i].value)/parseFloat(real_gdp_amt_data[i].value)*100).toFixed(1) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間投資）
		$("#gdp_title").append("<th style='text-align:center' colspan=6>【2】民間投資</th>");
		$("#gdp_title_2").append("<th class='warning' style='text-align:center' width='65px'>民間投資</th>");
		$("#gdp_title_2").append("<th class='info'  style='text-align:center' width='45px'>(%)</th>");
		// 填入表格內容（民間投資）
		var i = real_gpdi_crtb_data.length - 1;
		$.each(real_gpdi_crtb_data, function() {
			$("#"+real_gpdi_crtb_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_gpdi_crtb_data[i].value).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + (parseFloat(real_gpdi_amt_data[i].value)/parseFloat(real_gdp_amt_data[i].value)*100).toFixed(1) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間投資/住宅投資）
		$("#gdp_title_2").append("<th class='warning' style='text-align:center' width='65px'>(住宅)</th>");
		$("#gdp_title_2").append("<th class='info'  style='text-align:center' width='45px'>(%)</th>");
		// 填入表格內容（民間投資/住宅投資）
		var i = real_prfi_crtb_data.length - 1;
		$.each(real_prfi_crtb_data, function() {
			$("#"+real_prfi_crtb_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_prfi_crtb_data[i].value).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + (parseFloat(real_prfi_amt_data[i].value)/parseFloat(real_gdp_amt_data[i].value)*100).toFixed(1) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間投資/非住宅投資）
		$("#gdp_title_2").append("<th class='warning' style='text-align:center' width='65px'>(非住宅)</th>");
		$("#gdp_title_2").append("<th class='info'  style='text-align:center' width='45px'>(%)</th>");
		// 填入表格內容（民間投資/非住宅投資）
		var i = real_pnfi_crtb_data.length - 1;
		$.each(real_pnfi_crtb_data, function() {
			$("#"+real_pnfi_crtb_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_pnfi_crtb_data[i].value).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + (parseFloat(real_pnfi_amt_data[i].value)/parseFloat(real_gdp_amt_data[i].value)*100).toFixed(1) + "</td>"
			);
			i--;
		});
		// 填入表格標題（進口）
		$("#gdp_title").append("<th style='text-align:center' colspan=4>【3】進出口</th>");
		$("#gdp_title_2").append("<th class='warning' style='text-align:center' width='55px'>進口</th>");
		$("#gdp_title_2").append("<th class='info'  style='text-align:center' width='45px'>(%)</th>");
		// 填入表格內容（進口）
		var i = real_impgs_crtb_data.length - 1;
		$.each(real_impgs_crtb_data, function() {
			$("#"+real_impgs_crtb_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_impgs_crtb_data[i].value).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + (-parseFloat(real_impgs_amt_data[i].value)/parseFloat(real_gdp_amt_data[i].value)*100).toFixed(1) + "</td>"
			);
			i--;
		});
		// 填入表格標題（出口）
		$("#gdp_title_2").append("<th class='warning' style='text-align:center' width='55px'>出口</th>");
		$("#gdp_title_2").append("<th class='info'  style='text-align:center' width='45px'>(%)</th>");
		// 填入表格內容（出口）
		var i = real_expgs_crtb_data.length - 1;
		$.each(real_expgs_crtb_data, function() {
			$("#"+real_expgs_crtb_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_expgs_crtb_data[i].value).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + (parseFloat(real_expgs_amt_data[i].value)/parseFloat(real_gdp_amt_data[i].value)*100).toFixed(1) + "</td>"
			);
			i--;
		});
		// 填入表格標題（政府支出與投資）
		$("#gdp_title").append("<th style='text-align:center' colspan=2>【4】政府支出</th>");
		$("#gdp_title_2").append("<th class='warning' style='text-align:center' width='65px'>政府支出</th>");
		$("#gdp_title_2").append("<th class='info' style='text-align:center' width='45px'>(%)</th>");
		// 填入表格內容（政府支出與投資）
		var i = real_gce_crtb_data.length - 1;
		$.each(real_gce_crtb_data, function() {
			$("#"+real_gce_crtb_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_gce_crtb_data[i].value).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + (parseFloat(real_gce_amt_data[i].value)/parseFloat(real_gdp_amt_data[i].value)*100).toFixed(1) + "</td>"
			);
			i--;
		});
		// --------------------
		// 步驟二：繪製HighStock
		// --------------------
		var real_gdp_crtb_date_array = [];
		var real_gdp_crtb_array = [];
		var real_pce_crtb_array = [];
		var real_pcdg_crtb_array = [];
		var real_gpdi_crtb_array = [];
		var real_prfi_crtb_array = [];
		var real_pnfi_crtb_array = [];
		var real_impgs_crtb_array = [];
		var real_expgs_crtb_array = [];
		var real_gce_crtb_array = [];
		for (i = 0; i < real_gdp_crtb_data.length; i++) {
			real_gdp_crtb_date_array[i] = real_gdp_crtb_data[i].date;
			real_gdp_crtb_array[i] = parseFloat(real_gdp_crtb_data[i].value);
			real_pce_crtb_array[i] = parseFloat(real_pce_crtb_data[i].value);
			real_pcdg_crtb_array[i] = parseFloat(real_pcdg_crtb_data[i].value);
			real_gpdi_crtb_array[i] = parseFloat(real_gpdi_crtb_data[i].value);
			real_prfi_crtb_array[i] = parseFloat(real_prfi_crtb_data[i].value);
			real_pnfi_crtb_array[i] = parseFloat(real_pnfi_crtb_data[i].value);
			real_impgs_crtb_array[i] = parseFloat(real_impgs_crtb_data[i].value);
			real_expgs_crtb_array[i] = parseFloat(real_expgs_crtb_data[i].value);
			real_gce_crtb_array[i] = parseFloat(real_gce_crtb_data[i].value);
		};
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		$('.container#chart').highcharts({
			chart: {
				zoomType: 'xy'
			},
			title: {
				text: '實質GDP成長率 vs 分項貢獻度'
			},
			subtitle: {
				text: 'Source: St. Louis Fed'
			},
			xAxis: [{
				categories: real_gdp_crtb_date_array,
				tickmarkPlacement: 'on',
				tickInterval: 2,
				labels: {
					staggerLines: 2,
					step: 1,
					formatter: function () {
						if (this.value.substr(4, 6) === "-01-01") {
							return this.value.substr(0, 5) + "Q1";
						} else if (this.value.substr(4, 6) === "-04-01") {
							return this.value.substr(0, 5) + "Q2";
						} else if (this.value.substr(4, 6) === "-07-01") {
							return this.value.substr(0, 5) + "Q3";
						} else {
							return this.value.substr(0, 5) + "Q4";
						}
					}
				}
			}],
			yAxis: [{
				labels: {
					format: '{value}%'
				},
				title: {
					text: '實質GDP成長率(%)',
					style: {
						color: Highcharts.getOptions().colors[2]
					}
				}
			},{
				labels: {
					format: '{value}%'
				},
				title: {
					text: '分項貢獻度(%)',
					style: {
						color: Highcharts.getOptions().colors[6]
					}
				},
				opposite: true
			}],
			tooltip: {
				formatter: function () {
					var s = '<b>' + this.x + '</b>';
					$.each(this.points, function () {
						s += '<br/>' + this.series.name + ': ' +
						(this.y).toFixed(2) + '%';
					});
					return s;
				},
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
			plotOptions: {
				series: {
					marker: {
						enabled: false
					}
				}
			},
			series: [{
				name: '實質GDP成長率',
				type: 'spline',
				data: real_gdp_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				}
			}, {
				name: '民間消費',
				type: 'spline',
				data: real_pce_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'ShortDash',
				yAxis: 1
			}, {
				name: '耐久財',
				type: 'spline',
				data: real_pcdg_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}, {
				name: '民間投資',
				type: 'spline',
				data: real_gpdi_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'ShortDash',
				visible: false,
				yAxis: 1
			}, {
				name: '住宅',
				type: 'spline',
				data: real_prfi_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}, {
				name: '非住宅',
				type: 'spline',
				data: real_pnfi_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}, {
				name: '進口',
				type: 'spline',
				data: real_impgs_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'ShortDash',
				visible: false,
				yAxis: 1
			}, {
				name: '出口',
				type: 'spline',
				data: real_expgs_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'ShortDash',
				visible: false,
				yAxis: 1
			}, {
				name: '政府支出',
				type: 'spline',
				data: real_gce_crtb_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'ShortDash',
				visible: false,
				yAxis: 1
			}]
		});
		// HighChart程式碼結束位置
	});
};

// --------------------------
//  *** GDP成長率 ***
// --------------------------
function usa_economics_gdp() {
	$("#usa_eco_footer").html("");
	$("#usa_eco_footer").html("美國GDP佔全球1/4強，且民間消費佔比高達70%，讓美國穩坐全球最大進口國，其景氣榮枯牽動全球市場，<br>&nbsp&nbsp&nbsp&nbsp因此必須掌握其經濟情勢變化，並提前判斷貨幣政策風向。");
	$.when($.ajax("/usa_economics_real_gdp/"),
			$.ajax("/usa_economics_dollar_gdp/"),
			$.ajax("/usa_economics_real_pce/"),
			$.ajax("/usa_economics_real_pcdg/"),
			$.ajax("/usa_economics_real_gpdi/"),
			$.ajax("/usa_economics_real_prfi/"),
			$.ajax("/usa_economics_real_pnfi/"),
			$.ajax("/usa_economics_real_impgs/"),
			$.ajax("/usa_economics_real_expgs/"),
			$.ajax("/usa_economics_real_gce/"),
			$.ajax("/usa_economics_dollar_dpi/")
			).done(function(real_gdp, dollar_gdp, real_pce, real_pcdg, real_gpdi, real_prfi, real_pnfi, real_impgs, real_expgs, real_gce, dollar_dpi){
		// ------------------
		// 步驟一：填入表格資料
		// ------------------
		var real_gdp_data = real_gdp[0].observations;
		var dollar_gdp_data = dollar_gdp[0].observations;
		var real_pce_data = real_pce[0].observations;
		var real_pcdg_data = real_pcdg[0].observations;
		var real_gpdi_data = real_gpdi[0].observations;
		var real_prfi_data = real_prfi[0].observations;
		var real_pnfi_data = real_pnfi[0].observations;
		var real_impgs_data = real_impgs[0].observations;
		var real_expgs_data = real_expgs[0].observations;
		var real_gce_data = real_gce[0].observations;
		var dollar_dpi_data = dollar_dpi[0].observations;
		// 清空表格標題和內容
		$("#usa_economics_data_title").html("");
		$("#usa_economics_data").html("");
		// 填入表格標題（名目GDP成長率和GDP投資指標）
		$("#usa_economics_data_title").append("<tr class='info' id='gdp_title'>" +
			"<th style='text-align:center'>GDP(子)項目</th>" +
			"<th style='text-align:center' rowspan=2>GDP<br>投資指標</th>" +
			"<th style='text-align:center' rowspan=2>名目GDP<br>成長率</th></tr>" +
			"<tr class='info' id='gdp_title_2'><th style='text-align:center'>日期(每季)</th></tr>");
		// 填入表格內容（名目GDP成長率）
		var i = dollar_gdp_data.length - 1;
		$.each(dollar_gdp_data, function() {
			$("#usa_economics_data").append("<tr id=" + dollar_gdp_data[i].date + ">" +
				"<td style='text-align:center'>" + dollar_gdp_data[i].date + "</td>" +
				"<td style='text-align:center'>" + (parseFloat(dollar_gdp_data[i].value) - parseFloat(real_gdp_data[i].value)).toFixed(2) + "</td>" +
				"<td style='text-align:center'>" + parseFloat(dollar_gdp_data[i].value).toFixed(2) + "</td>" +
				"</tr>"
			);
			i--;
		});
		// 填入表格標題（實質GDP成長率）
		$("#gdp_title").append("<th style='text-align:center' rowspan=2>實質GDP<br>成長率</th>");
		// 填入表格內容（實質GDP成長率）
		var i = real_gdp_data.length - 1;
		$.each(real_gdp_data, function() {
			$("#"+real_gdp_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_gdp_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間消費）
		$("#gdp_title").append("<th style='text-align:center' colspan=2>【1】民間消費</th>");
		$("#gdp_title_2").append("<th style='text-align:center'>民間消費</th>");
		// 填入表格內容（民間消費）
		var i = real_pce_data.length - 1;
		$.each(real_pce_data, function() {
			$("#"+real_pce_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_pce_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間消費/耐久財）
		$("#gdp_title_2").append("<th style='text-align:center'>(耐久財)</th>");
		// 填入表格內容（民間消費/耐久財）
		var i = real_pcdg_data.length - 1;
		$.each(real_pcdg_data, function() {
			$("#"+real_pcdg_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_pcdg_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間投資）
		$("#gdp_title").append("<th style='text-align:center' colspan=3>【2】民間投資</th>");
		$("#gdp_title_2").append("<th style='text-align:center'>民間投資</th>");
		// 填入表格內容（民間投資）
		var i = real_gpdi_data.length - 1;
		$.each(real_gpdi_data, function() {
			$("#"+real_gpdi_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_gpdi_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間投資/住宅投資）
		$("#gdp_title_2").append("<th style='text-align:center'>(住宅)</th>");
		// 填入表格內容（民間投資/住宅投資）
		var i = real_prfi_data.length - 1;
		$.each(real_prfi_data, function() {
			$("#"+real_prfi_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_prfi_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（民間投資/非住宅投資）
		$("#gdp_title_2").append("<th style='text-align:center'>(非住宅)</th>");
		// 填入表格內容（民間投資/非住宅投資）
		var i = real_pnfi_data.length - 1;
		$.each(real_pnfi_data, function() {
			$("#"+real_pnfi_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_pnfi_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（進口）
		$("#gdp_title").append("<th style='text-align:center' colspan=2>【3】進出口</th>");
		$("#gdp_title_2").append("<th style='text-align:center'>進口</th>");
		// 填入表格內容（進口）
		var i = real_impgs_data.length - 1;
		$.each(real_impgs_data, function() {
			$("#"+real_impgs_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_impgs_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（出口）
		$("#gdp_title_2").append("<th style='text-align:center'>出口</th>");
		// 填入表格內容（出口）
		var i = real_expgs_data.length - 1;
		$.each(real_expgs_data, function() {
			$("#"+real_expgs_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_expgs_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（政府支出與投資）
		$("#gdp_title").append("<th style='text-align:center' rowspan=2>【4】政府<br>支出與投資</th>");
		// 填入表格內容（政府支出與投資）
		var i = real_gce_data.length - 1;
		$.each(real_gce_data, function() {
			$("#"+real_gce_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(real_gce_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（名目可支配所得）
		$("#gdp_title").append("<th style='text-align:center' rowspan=2>可支配<br>所得</th>");
		// 填入表格內容（名目可支配所得）
		var i = dollar_dpi_data.length - 1;
		$.each(dollar_dpi_data, function() {
			$("#"+dollar_dpi_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(dollar_dpi_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// --------------------
		// 步驟二：繪製HighStock
		// --------------------
		var dollar_gdp_date_array = [];
		var gdp_indicator_array = [];
		var real_pce_array = [];
		var real_pcdg_array = [];
		var real_gpdi_array = [];
		var real_prfi_array = [];
		var real_pnfi_array = [];
		var real_impgs_array = [];
		var real_gce_array = [];
		var dollar_dpi_array = [];
		for (i = 0; i < dollar_gdp_data.length; i++) {
			dollar_gdp_date_array[i] = dollar_gdp_data[i].date;
			gdp_indicator_array[i] = parseFloat(dollar_gdp_data[i].value) - parseFloat(real_gdp_data[i].value);
			real_pce_array[i] = parseFloat(real_pce_data[i].value);
			real_pcdg_array[i] = parseFloat(real_pcdg_data[i].value);
			real_gpdi_array[i] = parseFloat(real_gpdi_data[i].value);
			real_prfi_array[i] = parseFloat(real_prfi_data[i].value);
			real_pnfi_array[i] = parseFloat(real_pnfi_data[i].value);
			real_impgs_array[i] = parseFloat(real_impgs_data[i].value);
			real_gce_array[i] = parseFloat(real_gce_data[i].value);
			dollar_dpi_array[i] = parseFloat(dollar_dpi_data[i].value);
		};
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		$('.container#chart').highcharts({
			chart: {
				zoomType: 'xy'
			},
			title: {
				text: 'GDP投資指標 vs 分項成長率'
			},
			subtitle: {
				text: 'Source: St. Louis Fed'
			},
			xAxis: [{
				categories: dollar_gdp_date_array,
				tickmarkPlacement: 'on',
				tickInterval: 2,
				labels: {
					staggerLines: 2,
					step: 1,
					formatter: function () {
						if (this.value.substr(4, 6) === "-01-01") {
							return this.value.substr(0, 5) + "Q1";
						} else if (this.value.substr(4, 6) === "-04-01") {
							return this.value.substr(0, 5) + "Q2";
						} else if (this.value.substr(4, 6) === "-07-01") {
							return this.value.substr(0, 5) + "Q3";
						} else {
							return this.value.substr(0, 5) + "Q4";
						}
					}
				}
			}],
			yAxis: [{
				labels: {
					format: '{value}%'
				},
				title: {
					text: 'GDP投資指標(%)',
					style: {
						color: Highcharts.getOptions().colors[2]
					}
				}
			},{
				labels: {
					format: '{value}%'
				},
				title: {
					text: '分項成長率(%)',
					style: {
						color: Highcharts.getOptions().colors[6]
					}
				},
				opposite: true
			}],
			tooltip: {
				formatter: function () {
					var s = '<b>' + this.x + '</b>';
					$.each(this.points, function () {
						s += '<br/>' + this.series.name + ': ' +
						(this.y).toFixed(2) + '%';
					});
					return s;
				},
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
			plotOptions: {
				series: {
					marker: {
						enabled: false
					}
				}
			},
			series: [{
				name: 'GDP投資指標',
				type: 'column',
				data: gdp_indicator_array,
				tooltip: {
					valueSuffix: ' %'
				}
			}, {
				name: '民間消費',
				type: 'spline',
				data: real_pce_array,
				tooltip: {
					valueSuffix: ' %'
				},
				yAxis: 1
			}, {
				name: '耐久財',
				type: 'spline',
				data: real_pcdg_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}, {
				name: '民間投資',
				type: 'spline',
				data: real_gpdi_array,
				tooltip: {
					valueSuffix: ' %'
				},
				visible: false,
				yAxis: 1
			}, {
				name: '住宅',
				type: 'spline',
				data: real_prfi_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}, {
				name: '非住宅',
				type: 'spline',
				data: real_pnfi_array,
				tooltip: {
					valueSuffix: ' %'
				},
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}, {
				name: '進口',
				type: 'spline',
				data: real_impgs_array,
				tooltip: {
					valueSuffix: ' %'
				},
				visible: false,
				yAxis: 1
			}, {
				name: '政府支出',
				type: 'spline',
				data: real_gce_array,
				tooltip: {
					valueSuffix: ' %'
				},
				visible: false,
				yAxis: 1
			}, {
				name: '可支配所得',
				type: 'spline',
				data: dollar_dpi_array,
				tooltip: {
					valueSuffix: ' %'
				},
				visible: false,
				yAxis: 1
			}]
		});
		// HighChart程式碼結束位置
	});
};

// -------------------------
//  *** 失業率趨勢 ***
// -------------------------
function usa_economics_unrate() {
	$("#usa_eco_footer").html("");
	$("#usa_eco_footer").html("失業率雖然是股市的落後指標，但失業率攀頂往往是股市最佳進場點；當中短期失業率減緩，則透露整體失業將好轉。<br>&nbsp&nbsp&nbsp&nbsp應用方式：高失業率進場，低失業率獲利了結。");
	$.when($.ajax("/usa_economics_civilian_unemployment_rate/"),
		$.ajax("/usa_economics_civilians_unemployed_lt5/"),
		$.ajax("/usa_economics_civilians_unemployed_5to14/"),
		$.ajax("/usa_economics_civilians_unemployed_15t26/"),
		$.ajax("/usa_economics_civilians_unemployed_27ov/"),
		$.ajax("/usa_economics_sp500_index_monthly/")
	).done(function(unrate, uemplt5, uemp5to14, uemp15t26, uemp27ov, sp500m) {
		// ------------------
		// 步驟一：填入表格資料
		// ------------------
		var unrate_data = unrate[0].observations;
		var uemplt5_data = uemplt5[0].observations;
		var uemp5to14_data = uemp5to14[0].observations;
		var uemp15t26_data = uemp15t26[0].observations;
		var uemp27ov_data = uemp27ov[0].observations;
		var uemp27ov_data = uemp27ov[0].observations;
		var sp500m_data = sp500m[0].observations;
		// 清空表格標題和內容
		$("#usa_economics_data_title").html("");
		$("#usa_economics_data").html("");
		// 填入表格標題（失業率）
		$("#usa_economics_data_title").append("<tr class='info' id='unrate_title'>" +
			"<th style='text-align:center'>日期(每月)</th>" +
			"<th style='text-align:center' width='100px'>失業率(%)</th>" +
			"</tr>");
		// 填入表格內容（失業率）
		var i = unrate_data.length - 1;
		$.each(unrate_data, function() {
			$("#usa_economics_data").append("<tr id=" + unrate_data[i].date + ">" +
				"<td style='text-align:center'>" + unrate_data[i].date + "</td>" +
				"<td style='text-align:center'>" + parseFloat(unrate_data[i].value).toFixed(2) + "</td>" +
				"</tr>"
			);
			i--;
		});
		// 填入表格標題（失業人數,低於5週）
		$("#unrate_title").append("<th style='text-align:center' width='150px'>失業人數(千人)<br>待業週數低於5週</th>");
		// 填入表格內容（失業人數,低於5週）
		var i = uemplt5_data.length - 1;
		$.each(uemplt5_data, function() {
			$("#"+uemplt5_data[i].date).append(
				"<td style='text-align:center'>" + number_format(uemplt5_data[i].value) + "</td>"
			);
			i--;
		});
		// 填入表格標題（失業人數,5～14週）
		$("#unrate_title").append("<th style='text-align:center' width='150px'>失業人數(千人)<br>待業週數5～14週</th>");
		// 填入表格內容（失業人數,5～14週）
		var i = uemp5to14_data.length - 1;
		$.each(uemp5to14_data, function() {
			$("#"+uemp5to14_data[i].date).append(
				"<td style='text-align:center'>" + number_format(uemp5to14_data[i].value) + "</td>"
			);
			i--;
		});
		// 填入表格標題（失業人數,15～26週）
		$("#unrate_title").append("<th style='text-align:center' width='150px'>失業人數(千人)<br>待業週數15～26週</th>");
		// 填入表格內容（失業人數,15～26週）
		var i = uemp15t26_data.length - 1;
		$.each(uemp15t26_data, function() {
			$("#"+uemp15t26_data[i].date).append(
				"<td style='text-align:center'>" + number_format(uemp15t26_data[i].value) + "</td>"
			);
			i--;
		});
		// 填入表格標題（失業人數,27週以上）
		$("#unrate_title").append("<th style='text-align:center' width='150px'>失業人數(千人)<br>待業週數27週以上</th>");
		// 填入表格內容（失業人數,27週以上）
		var i = uemp27ov_data.length - 1;
		$.each(uemp27ov_data, function() {
			$("#"+uemp27ov_data[i].date).append(
				"<td style='text-align:center'>" + number_format(uemp27ov_data[i].value) + "</td>"
			);
			i--;
		});
		// 填入表格標題（S&P500月收盤價）
		$("#unrate_title").append("<th style='text-align:center' width='100px'>S&P500<br>月收盤價</th>");
		// 填入表格內容（S&P500月收盤價）
		var i = sp500m_data.length - 1;
		$.each(sp500m_data, function() {
			$("#"+sp500m_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(sp500m_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// --------------------
		// 步驟二：繪製HighStock
		// --------------------
		var unrate_date_array = [];
		var unrate_array = [];
		var uemplt5_array = [];
		var uemp5to14_array = [];
		var uemp15t26_array = [];
		var uemp27ov_array = [];
		var sp500m_array = [];
		for (i = 0; i < unrate_data.length; i++) {
			unrate_date_array[i] = unrate_data[i].date;
			unrate_array[i] = parseFloat(unrate_data[i].value);
			uemplt5_array[i] = parseInt(uemplt5_data[i].value);
			uemp5to14_array[i] = parseInt(uemp5to14_data[i].value);
			uemp15t26_array[i] = parseInt(uemp15t26_data[i].value);
			uemp27ov_array[i] = parseInt(uemp27ov_data[i].value);
			sp500m_array[i] = parseInt(sp500m_data[i].value);
		};
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		$('.container#chart').highcharts({
			chart: {
				zoomType: 'xy'
			},
			title: {
				text: '失業率 & 失業人口待業週數'
			},
			subtitle: {
				text: 'Source: St. Louis Fed'
			},
			xAxis: [{
				categories: unrate_date_array,
				tickmarkPlacement: 'on',
				tickInterval: 6,
				labels: {
					staggerLines: 2,
					step: 1
				}
			}],
			yAxis: [{
				labels: {
					format: '{value}%'
				},
				title: {
					text: '失業率',
					style: {
						color: Highcharts.getOptions().colors[5]
					}
				}
			},{
				labels: {
					format: '{value}'
				},
				title: {
					text: '失業人數(千人)',
					style: {
						color: Highcharts.getOptions().colors[6]
					}
				},
				opposite: true
			},{
				labels: {
					format: '{value}'
				},
				title: {
					text: 'S&P500指數',
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
			plotOptions: {
				series: {
					marker: {
						enabled: false
					}
				}
			},
			series: [{
				name: '失業率',
				type: 'spline',
				data: unrate_array
			}, {
				name: '低於5週',
				type: 'spline',
				data: uemplt5_array,
				dashStyle: 'shortdot',
				visible: true,
				yAxis: 1
			}, {
				name: '5-14週',
				type: 'spline',
				data: uemp5to14_array,
				dashStyle: 'shortdot',
				visible: true,
				yAxis: 1
			}, {
				name: '15-26週',
				type: 'spline',
				data: uemp15t26_array,
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}, {
				name: '27週以上',
				type: 'spline',
				data: uemp27ov_array,
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}, {
				name: 'S&P500',
				type: 'spline',
				data: sp500m_array,
				visible: false,
				yAxis: 2
			}]
		});
		// HighChart程式碼結束位置
	});
};

// -------------------------
//  *** 通膨 & 利率 ***
// -------------------------
function usa_economics_inflation() {
	$("#usa_eco_footer").html("");
	$("#usa_eco_footer").html("貨幣政策的目標，是讓核心通膨維持在可以促進經濟發展的區間，對美國而言，大約是2~2.5%之間。<br>&nbsp&nbsp&nbsp&nbsp而當資產泡沫或經濟風暴發生時，貨幣政策的首要目標，就是確保通膨能確實發生，以抵銷通縮危機。");
	$.when($.ajax("/usa_economics_dollar_cpi/"),
		$.ajax("/usa_economics_core_cpi/"),
		$.ajax("/usa_economics_10yr_yield/"),
		$.ajax("/usa_economics_30yr_mortg_rate/")
	).done(function(dollar_cpi, core_cpi, yr10_yield, yr30_mortg_rate) {
		// ------------------
		// 步驟一：填入表格資料
		// ------------------
		var dollar_cpi_data = dollar_cpi[0].observations;
		var core_cpi_data = core_cpi[0].observations;
		var yr10_yield_data = yr10_yield[0].observations;
		var yr30_mortg_rate_data = yr30_mortg_rate[0].observations;
		// 清空表格標題和內容
		$("#usa_economics_data_title").html("");
		$("#usa_economics_data").html("");
		// 填入表格標題（名目CPI）
		$("#usa_economics_data_title").append("<tr class='info' id='inflation_title'>" +
			"<th style='text-align:center'>日期(每月) / 項目</th>" +
			"<th style='text-align:center' width='150px'>名目CPI年增率</th>" +
			"</tr>");
		// 填入表格內容（名目CPI）
		var i = dollar_cpi_data.length - 1;
		$.each(dollar_cpi_data, function() {
			$("#usa_economics_data").append("<tr id=" + dollar_cpi_data[i].date + ">" +
				"<td style='text-align:center'>" + dollar_cpi_data[i].date + "</td>" +
				"<td style='text-align:center'>" + parseFloat(dollar_cpi_data[i].value).toFixed(4) + "</td>" +
				"</tr>"
			);
			i--;
		});
		// 填入表格標題（核心CPI）
		$("#inflation_title").append("<th style='text-align:center' width='150px'>核心CPI年增率</th>");
		// 填入表格內容（核心CPI）
		var i = core_cpi_data.length - 1;
		$.each(core_cpi_data, function() {
			$("#"+core_cpi_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(core_cpi_data[i].value).toFixed(4) + "</td>"
			);
			i--;
		});
		// 填入表格標題（10年期公債殖利率）
		$("#inflation_title").append("<th style='text-align:center' width='150px'>10年期公債殖利率</th>");
		// 填入表格內容（10年期公債殖利率）
		var i = yr10_yield_data.length - 1;
		$.each(yr10_yield_data, function() {
			$("#"+yr10_yield_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(yr10_yield_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（30年期房貸利率）
		$("#inflation_title").append("<th style='text-align:center' width='150px'>30年期房貸利率</th>");
		// 填入表格內容（30年期房貸利率）
		var i = yr30_mortg_rate_data.length - 1;
		$.each(yr30_mortg_rate_data, function() {
			$("#"+yr30_mortg_rate_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(yr30_mortg_rate_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// --------------------
		// 步驟二：繪製HighStock
		// --------------------
		var dollar_cpi_date_array = [];
		var dollar_cpi_array = [];
		var core_cpi_array = [];
		var yr10_yield_array = [];
		var yr30_mortg_rate_array = [];
		for (i = 0; i < dollar_cpi_data.length; i++) {
			dollar_cpi_date_array[i] = dollar_cpi_data[i].date;
			dollar_cpi_array[i] = parseFloat(dollar_cpi_data[i].value);
			core_cpi_array[i] = parseFloat(core_cpi_data[i].value);
			yr10_yield_array[i] = parseFloat(yr10_yield_data[i].value);
			yr30_mortg_rate_array[i] = parseFloat(yr30_mortg_rate_data[i].value);
		};
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		$('.container#chart').highcharts({
			chart: {
				zoomType: 'xy'
			},
			title: {
				text: '通膨 & 利率'
			},
			subtitle: {
				text: 'Source: St. Louis Fed'
			},
			xAxis: [{
				categories: dollar_cpi_date_array,
				tickmarkPlacement: 'on',
				tickInterval: 6,
				labels: {
					staggerLines: 2,
					step: 1
				}
			}],
			yAxis: [{
				labels: {
					format: '{value}%'
				},
				title: {
					text: '消費者物價指數(CPI)',
					style: {
						color: Highcharts.getOptions().colors[5]
					}
				}
			},{
				labels: {
					format: '{value}%'
				},
				title: {
					text: '利率',
					style: {
						color: Highcharts.getOptions().colors[6]
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
			plotOptions: {
				series: {
					marker: {
						enabled: false
					}
				}
			},
			series: [{
				name: '名目CPI',
				type: 'spline',
				data: dollar_cpi_array,
				dashStyle: 'shortdot',
				visible: false
			}, {
				name: '核心CPI',
				type: 'spline',
				data: core_cpi_array
			}, {
				name: '10yr公債殖利率',
				type: 'spline',
				data: yr10_yield_array,
				dashStyle: 'shortdot',
				visible: true,
				yAxis: 1
			}, {
				name: '30yr房貸利率',
				type: 'spline',
				data: yr30_mortg_rate_array,
				dashStyle: 'shortdot',
				visible: false,
				yAxis: 1
			}]
		});
		// HighChart程式碼結束位置
	});
};

// -------------------------
//  *** 美元指數 & 匯率 ***
// -------------------------
function usa_economics_fxrate() {
	$("#usa_eco_footer").html("");
	$("#usa_eco_footer").html("美元目前仍是全球最重要的儲備貨幣，因此當市場風險厭惡情緒提高時，熱錢往往會推升避險貨幣(ex.美元、日圓)走揚。");
	$.when($.ajax("/usa_economics_us_dollar_index/"),
		$.ajax("/usa_economics_euro_exchange_rate/"),
		$.ajax("/usa_economics_jpy_exchange_rate/"),
		$.ajax("/usa_economics_cny_exchange_rate/"),
		$.ajax("/usa_economics_twd_exchange_rate/"),
		$.ajax("/usa_economics_krw_exchange_rate/"),
		$.ajax("/usa_economics_aud_exchange_rate/"),
		$.ajax("/usa_economics_cboe_vix_index/")
	).done(function(us_dollar_index, euro_exchange_rate, jpy_exchange_rate, cny_exchange_rate, twd_exchange_rate, krw_exchange_rate, aud_exchange_rate, cboe_vix_index) {
		// ------------------
		// 步驟一：填入表格資料
		// ------------------
		var usd_data = us_dollar_index[0].observations;
		var euro_data = euro_exchange_rate[0].observations;
		var jpy_data = jpy_exchange_rate[0].observations;
		var cny_data = cny_exchange_rate[0].observations;
		var twd_data = twd_exchange_rate[0].observations;
		var krw_data = krw_exchange_rate[0].observations;
		var aud_data = aud_exchange_rate[0].observations;
		var vix_data = cboe_vix_index[0].observations;
		// 清空表格標題和內容
		$("#usa_economics_data_title").html("");
		$("#usa_economics_data").html("");
		// 填入表格標題（美元指數）
		$("#usa_economics_data_title").append("<tr class='info' id='fxrate_title'>" +
			"<th style='text-align:center'>日期(每週) / 貨幣別</th>" +
			"<th style='text-align:center' width='100px'>美元指數<br>(DXY)</th>" +
			"</tr>");
		// 填入表格內容（美元指數）
		var i = usd_data.length - 1;
		$.each(usd_data, function() {
			$("#usa_economics_data").append("<tr id=" + usd_data[i].date + ">" +
				"<td style='text-align:center'>" + usd_data[i].date + "</td>" +
				"<td style='text-align:center'>" + parseFloat(usd_data[i].value).toFixed(2) + "</td>" +
				"</tr>"
			);
			i--;
		});
		// 填入表格標題（歐元匯率）
		$("#fxrate_title").append("<th style='text-align:center' width='100px'>歐元<br>(EUR)</th>");
		// 填入表格內容（歐元匯率）
		var i = euro_data.length - 1;
		$.each(euro_data, function() {
			$("#"+euro_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(euro_data[i].value).toFixed(4) + "</td>"
			);
			i--;
		});
		// 填入表格標題（日元匯率）
		$("#fxrate_title").append("<th style='text-align:center' width='100px'>日圓<br>(YEN)</th>");
		// 填入表格內容（日元匯率）
		var i = jpy_data.length - 1;
		$.each(jpy_data, function() {
			$("#"+jpy_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(jpy_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（人民幣匯率）
		$("#fxrate_title").append("<th style='text-align:center' width='100px'>人民幣<br>(CNY)</th>");
		// 填入表格內容（人民幣匯率）
		var i = cny_data.length - 1;
		$.each(cny_data, function() {
			$("#"+cny_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(cny_data[i].value).toFixed(4) + "</td>"
			);
			i--;
		});
		// 填入表格標題（新台幣匯率）
		$("#fxrate_title").append("<th style='text-align:center' width='100px'>新台幣<br>(TWD)</th>");
		// 填入表格內容（新台幣匯率）
		var i = twd_data.length - 1;
		$.each(twd_data, function() {
			$("#"+twd_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(twd_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// 填入表格標題（韓圜匯率）
		$("#fxrate_title").append("<th style='text-align:center' width='100px'>韓圜<br>(KRW)</th>");
		// 填入表格內容（韓圜匯率）
		var i = krw_data.length - 1;
		$.each(krw_data, function() {
			$("#"+krw_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(krw_data[i].value).toFixed(1) + "</td>"
			);
			i--;
		});
		// 填入表格標題（澳幣匯率）
		$("#fxrate_title").append("<th style='text-align:center' width='100px'>澳幣<br>(AUD)</th>");
		// 填入表格內容（澳幣匯率）
		var i = aud_data.length - 1;
		$.each(aud_data, function() {
			$("#"+aud_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(aud_data[i].value).toFixed(4) + "</td>"
			);
			i--;
		});
		// 填入表格標題（VIX指數）
		$("#fxrate_title").append("<th style='text-align:center' width='100px'>恐慌指數<br>(VIX)</th>");
		// 填入表格內容（VIX指數）
		var i = vix_data.length - 1;
		$.each(vix_data, function() {
			$("#"+vix_data[i].date).append(
				"<td style='text-align:center'>" + parseFloat(vix_data[i].value).toFixed(2) + "</td>"
			);
			i--;
		});
		// --------------------
		// 步驟二：繪製HighStock
		// --------------------
		var usd_date_array = [];
		var usd_array = [];
		var euro_array = [];
		var jpy_array = [];
		var cny_array = [];
		var twd_array = [];
		var krw_array = [];
		var aud_array = [];
		var vix_array = [];
		for (i = 0; i < usd_data.length; i++) {
			usd_date_array[i] = usd_data[i].date;
			usd_array[i] = parseFloat(usd_data[i].value);
			euro_array[i] = parseFloat(euro_data[i].value);
			jpy_array[i] = parseFloat(jpy_data[i].value);
			cny_array[i] = parseFloat(cny_data[i].value);
			twd_array[i] = parseFloat(twd_data[i].value);
			krw_array[i] = parseFloat(krw_data[i].value);
			aud_array[i] = parseFloat(aud_data[i].value);
			vix_array[i] = parseFloat(vix_data[i].value);
		};
		// 載入Highchart Dark-unica theme
		Highcharts.setOptions(Highcharts.theme);
		// 貼上HighChart的程式碼
		$('.container#chart').highcharts({
			chart: {
				zoomType: 'xy'
			},
			title: {
				text: '美元指數 & 匯率 & 恐慌指數'
			},
			subtitle: {
				text: 'Source: St. Louis Fed'
			},
			xAxis: [{
				categories: usd_date_array,
				tickmarkPlacement: 'on',
				tickInterval: 26,
				labels: {
					staggerLines: 2,
					step: 1
				}
			}],
			yAxis: [{
				labels: {
					format: '{value}'
				},
				title: {
					text: '美元指數',
					style: {
						color: Highcharts.getOptions().colors[5]
					}
				}
			},{
				labels: {
					format: '{value}'
				},
				title: {
					text: '匯率 / 恐慌指數',
					style: {
						color: Highcharts.getOptions().colors[6]
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
			plotOptions: {
				series: {
					marker: {
						enabled: false
					}
				}
			},
			series: [{
				name: '美元指數',
				type: 'spline',
				data: usd_array
			}, {
				name: '歐元',
				type: 'spline',
				data: euro_array,
				visible: false,
				yAxis: 1
			}, {
				name: '日圓',
				type: 'spline',
				data: jpy_array,
				visible: true,
				yAxis: 1
			}, {
				name: '人民幣',
				type: 'spline',
				data: cny_array,
				visible: false,
				yAxis: 1
			}, {
				name: '新台幣',
				type: 'spline',
				data: twd_array,
				visible: false,
				yAxis: 1
			}, {
				name: '韓圜',
				type: 'spline',
				data: krw_array,
				visible: false,
				yAxis: 1
			}, {
				name: '澳幣',
				type: 'spline',
				data: aud_array,
				visible: false,
				yAxis: 1
			}, {
				name: '恐慌指數',
				type: 'spline',
				data: vix_array,
				visible: false,
				yAxis: 1
			}]
		});
		// HighChart程式碼結束位置
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