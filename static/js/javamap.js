$(function () {
   $(document).ready(function(){
        $.getJSON('/map/',function(data){
			   var chart = new Highcharts.Chart({
					chart: {
						type: 'line',
						renderTo: 'javachart',
						marginRight: 130,
						marginBottom: 25
					},
					title: {
						text: '每月收益',
						x: -20 //center
					},
					subtitle: {
						text: '查看各个月的收益情况',
						x: -20
					},
					xAxis: {
						categories: ['一月', '二月', '三月', '四月', '五月', '六月',
							'七月', '八月', '九月', '十月', '十一月', '十二月']
					},
					yAxis: {
						title: {
							text: '钱(元)'
						},
						plotLines: [{
							value: 0,
							width: 1,
							color: '#808080'
						}]
					},
					tooltip: {
						valueSuffix: '元'
					},
					legend: {
						layout: 'vertical',
						align: 'right',
						verticalAlign: 'top',
						x: -10,
						y: 100,
						borderWidth: 0
					},
					series:data, 
				});											
        });
    });
});