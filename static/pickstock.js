$(document).ready(function() {
	// pickstock_bluechip();
});

//將數字轉成帶有千分位符號的格式
function number_format(n) {
	n += "";
	var arr = n.split(".");
	var re = /(\d{1,3})(?=(\d{3})+$)/g;
	return arr[0].replace(re,"$1,") + (arr.length == 2 ? "."+arr[1] : "");
};

$('#start_filter').click(function(){
	$.ajax({
		url:"/pickstock_bluechip/",
		type: "GET",
		data: $('#fins_filiters').serializeArray(),
		dataType: "json",
		success: function(data) {
			console.log(data);
			// 表格的標題
			$("#pickstock_title").html("<tr class='info'>" +
				"<th class='text-center' rowspan=2 width='55px'>股票<br>代號</th>" +
				"<th class='text-center' rowspan=2 width='70px'>股票<br>名稱</th>" +
				"<th class='text-center' colspan=4>營益率(%)</th>" +
				"<th class='text-center' colspan=4>EPS(元)</th>" +
				"<th class='text-center' rowspan=2>最近4季<br>自由現金流</th>" +
				"<th class='text-center' colspan=3>月營收年增率(%)</th>" +
				"<th class='text-center' colspan=2>" + data.forcast_yr + "EPS(元)</th>" +
				"<th class='text-center' rowspan=2 width='60px'>最新<br>收盤價</th>" +
				"<th class='text-center' colspan=2>本益比區間</th>" +
				"<th class='text-center' rowspan=2 width='60px'>上年度<br>股利(元)</th>" +
				"<th class='text-center' rowspan=2 width='60px'>上年度<br>配息率</th>" +
				"<th class='text-center' rowspan=2 width='60px'>預估<br>配息(元)</th>" +
				"<th class='text-center' rowspan=2 width='60px'>預估<br>殖利率</th>" +
				"</tr>" +
				"<tr class='info'>" +
				"<th class='text-center' width='65px'>" + data.pickstock_qtrname[0] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_qtrname[1] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_qtrname[2] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_qtrname[3] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_qtrname[0] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_qtrname[1] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_qtrname[2] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_qtrname[3] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_mthname[0] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_mthname[1] + "</th>" +
				"<th class='text-center' width='65px'>" + data.pickstock_mthname[2] + "</th>" +
				"<th class='text-center' width='55px'>" + "樂觀" + "</th>" +
				"<th class='text-center' width='55px'>" + "保守" + "</th>" +
				"<th class='text-center' width='55px'>" + "樂觀" + "</th>" +
				"<th class='text-center' width='55px'>" + "保守" + "</th>" +
				"</tr>"
			);
			$("#pickstock").html("");
			// 將資料按照股代號順序填入表格內容
			var i = 0;
			$.each(data.pickstock_id, function() {
				$("#pickstock").append("<tr>" +
					"<td style='text-align:center'><a href='http://127.0.0.1:8000/assign_task/?q=" +
						 data.pickstock_id[i] + "&button=Search_finrpts' target='_blank'>" + data.pickstock_id[i] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_cname[i] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_opm[i][0] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_opm[i][1] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_opm[i][2] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_opm[i][3] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_eps[i][0] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_eps[i][1] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_eps[i][2] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_eps[i][3] + "</td>" +
					"<td style='text-align:center'>" + number_format(data.pickstock_freecf_sum[i]) + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_salesyoy[i][0] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_salesyoy[i][1] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_salesyoy[i][2] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_forcast_yr_eps[i].toFixed(2) + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_forcast_yr_eps_conservative[i].toFixed(2) + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_dailyprice[i] + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_forward_per[i].toFixed(2) + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_forward_per_conservative[i].toFixed(2) + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_dividends[i].toFixed(2) + "</td>" +
					"<td style='text-align:center'>" + (data.pickstock_payoutratio[i]*100).toFixed(0) + "%</td>" +
					"<td style='text-align:center'>" + data.pickstock_forcast_dividends[i].toFixed(2) + "</td>" +
					"<td style='text-align:center'>" + data.pickstock_forcast_yield[i].toFixed(1) + "%</td>" +
					"</tr>"
				);
				i++;
			});
			alert("Hello, 本次共挑出 " + data.pickstock_id.length.toString() + " 檔個股.");
		},
		error: function() {
			alert("ERROR!!!");
		}
	});
});