$(document).ready(function() {
	world_economics_gdp();
	$("li#world_economics_gdp").click(function() {
		world_economics_gdp();
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
function world_economics_gdp() {
	$.when($.ajax("/world_real_gdp_usa/"),
		$.ajax("/world_real_gdp_eurozone/"),
		$.ajax("/world_real_gdp_china/"),
		$.ajax("/world_real_gdp_japan/"),
		$.ajax("/world_real_gdp_germany/"),
		$.ajax("/world_real_gdp_france/"),
		$.ajax("/world_real_gdp_uk/"),
		$.ajax("/world_real_gdp_brazil/"),
		$.ajax("/world_real_gdp_italy/"),
		$.ajax("/world_real_gdp_india/")
		).done(function(usa_real_gdp,eurozone_real_gdp,china_real_gdp,japan_real_gdp,germany_real_gdp,
			france_real_gdp,uk_real_gdp,brazil_real_gdp,italy_real_gdp,india_real_gdp){
		console.log(germany_real_gdp);
		// ------------------
		// 步驟一：填入表格資料
		// ------------------
		var usa_real_gdp_data = usa_real_gdp[0].observations;
		var eurozone_real_gdp_data = eurozone_real_gdp[0].observations;
		var china_real_gdp_data = china_real_gdp[0].observations;
		var japan_real_gdp_data = japan_real_gdp[0].observations;
		var germany_real_gdp_data = germany_real_gdp[0].observations;
		var france_real_gdp_data = france_real_gdp[0].observations;
		var uk_real_gdp_data = uk_real_gdp[0].observations;
		var brazil_real_gdp_data = brazil_real_gdp[0].observations;
		var italy_real_gdp_data = italy_real_gdp[0].observations;
		var india_real_gdp_data = india_real_gdp[0].observations;
		// 清空表格標題和內容
		$("#world_economics_data_title").html("");
		$("#world_economics_data").html("");
		// 填入表格標題（實質GDP成長率）
		$("#world_economics_data_title").append("<tr class='info' id='world_title'>" +
			"<th style='text-align:center'>GDP成長率</th>" +
			"<th style='text-align:center' colspan=18>國家（依GDP總值排序，有*號標註者為名目GDP，此處成長率即慣用的QoQ值）</th></tr>" +
			"<tr id='world_title_2'>" +
			"<th class='info' style='text-align:center'>日期(每季)</th>" + 
			"<th class='warning' style='text-align:center' width='60px'>美國</th>" +
			"<th class='info' style='text-align:center' width='60px'>歐元區</th>" +
			"<th class='warning' style='text-align:center' width='60px'>中國*</th>" +
			"<th class='info' style='text-align:center' width='60px'>日本</th>" +
			"<th class='warning' style='text-align:center' width='60px'>德國</th>" +
			"<th class='info' style='text-align:center' width='60px'>法國</th>" +
			"<th class='warning' style='text-align:center' width='60px'>英國</th>" +
			"<th class='info' style='text-align:center' width='60px'>巴西</th>" +
			"<th class='warning' style='text-align:center' width='60px'>俄羅斯</th>" +
			"<th class='info' style='text-align:center' width='60px'>義大利</th>" +
			"<th class='warning' style='text-align:center' width='60px'>印度</th>" +
			"<th class='info' style='text-align:center' width='60px'>加拿大</th>" +
			"<th class='warning' style='text-align:center' width='60px'>澳洲</th>" +
			"<th class='info' style='text-align:center' width='60px'>西班牙</th>" +
			"<th class='warning' style='text-align:center' width='60px'>南韓</th>" +
			"<th class='info' style='text-align:center' width='60px'>墨西哥</th>" +
			"<th class='warning' style='text-align:center' width='60px'>印尼</th>" +
			"<th class='info' style='text-align:center' width='60px'>土耳其</th>" +
			"</tr>");
		// 填入表格內容（實質GDP成長率-美國）
		var i = usa_real_gdp_data.length - 1;
		$.each(usa_real_gdp_data, function() {
			$("#world_economics_data").append("<tr id=" + usa_real_gdp_data[i].date + ">" +
				"<td style='text-align:center'>" + usa_real_gdp_data[i].date + "</td>" +
				"<td style='text-align:center'>" + parseFloat(usa_real_gdp_data[i].value).toFixed(2) + "</td>" +
				"</tr>"
			);
			i--;
		});
		// 替美國以外的國家建立空白儲存格
		var i = usa_real_gdp_data.length - 1;
		$.each(usa_real_gdp_data, function() {
			$("#"+usa_real_gdp_data[i].date).append(
				"<td style='text-align:center' id=eurozone_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=china_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=japan_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=germany_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=france_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=uk_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=brazil_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=russia_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=italy_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=india_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=canada_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=australia_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=spain_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=korea_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=mexico_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=indonesia_" + usa_real_gdp_data[i].date + ">n.a.</td>" +
				"<td style='text-align:center' id=turkey_" + usa_real_gdp_data[i].date + ">n.a.</td>"
			);
			i--;
		});
		// 填入表格內容（實質GDP成長率-歐元區）
		var i = eurozone_real_gdp_data.length - 1;
		$.each(eurozone_real_gdp_data, function() {
			$("#eurozone_"+eurozone_real_gdp_data[i].date).text(
				parseFloat(eurozone_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
		// 填入表格內容（名目GDP成長率-中國）
		var i = china_real_gdp_data.length - 1;
		$.each(china_real_gdp_data, function() {
			$("#china_"+china_real_gdp_data[i].date).text(
				parseFloat(china_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
		// // 填入表格內容（實質GDP成長率-日本）
		var i = japan_real_gdp_data.length - 1;
		$.each(japan_real_gdp_data, function() {
			$("#japan_"+japan_real_gdp_data[i].date).text(
				parseFloat(japan_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
		// // 填入表格內容（實質GDP成長率-德國）
		var i = germany_real_gdp_data.length - 1;
		$.each(germany_real_gdp_data, function() {
			$("#germany_"+germany_real_gdp_data[i].date).text(
				parseFloat(germany_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
		// // 填入表格內容（實質GDP成長率-法國）
		var i = france_real_gdp_data.length - 1;
		$.each(france_real_gdp_data, function() {
			$("#france_"+france_real_gdp_data[i].date).text(
				parseFloat(france_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
		// // 填入表格內容（實質GDP成長率-英國）
		var i = uk_real_gdp_data.length - 1;
		$.each(uk_real_gdp_data, function() {
			$("#uk_"+uk_real_gdp_data[i].date).text(
				parseFloat(uk_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
		// // 填入表格內容（實質GDP成長率-巴西）
		var i = brazil_real_gdp_data.length - 1;
		$.each(brazil_real_gdp_data, function() {
			$("#brazil_"+brazil_real_gdp_data[i].date).text(
				parseFloat(brazil_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
		// // 填入表格內容（實質GDP成長率-義大利）
		var i = italy_real_gdp_data.length - 1;
		$.each(italy_real_gdp_data, function() {
			$("#italy_"+italy_real_gdp_data[i].date).text(
				parseFloat(italy_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
		// // 填入表格內容（實質GDP成長率-印度）
		var i = india_real_gdp_data.length - 1;
		$.each(india_real_gdp_data, function() {
			$("#india_"+india_real_gdp_data[i].date).text(
				parseFloat(india_real_gdp_data[i].value).toFixed(2)
			);
			i--;
		});
	});
};