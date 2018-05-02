weibo_user_signup = {
     title: {
        text: '微博粉丝用户注册分布情况',
        subtext: '微博爬虫统计',
        left: 'center',
        top: '0'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                color: '#999'
            }
        }
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    legend: {
        data:['注册人数','百分比'],
        x: 'left'
    },
    xAxis: [
        {
            type: 'category',
            data: ['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018'],
            axisPointer: {
                type: 'shadow'
            }
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '注册人数',
            min: 0,
            max: 30,
            interval: 3,
            axisLabel: {
                formatter: '{value} 人'
            }
        },
        {
            type: 'value',
            name: '百分比',
            min: 0,
            max: 50,
            interval: 5,
            axisLabel: {
                formatter: '{value} %'
            }
        }
    ],
    series: [
        {
            name:'注册人数',
            type:'bar',
            data:[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8,]
        },
        {
            name:'百分比',
            type:'line',
            yAxisIndex: 1,
            data:[2.0, 2.2, 3.3, 4.5, 5, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
        }
    ]
};


$("#bt_weibo_user_signup").click(
    function () {
        $(".user_info").hide();
        $("#weibo_user_signup").show();
        var chart = echarts.init(document.getElementById('weibo_user_signup'));
        var ucid = GetUrlParam('ucid');
        $.ajax({
            type: 'get',
            url: API_HOST + '/api/user/signup_time?ucid=' + ucid,
            data: '',
            dataType: 'json',
            success: function (data) {
                weibo_user_signup.series[0].data = data['signup_list'];
                weibo_user_signup.series[1].data = data['percent_list'];

                chart.setOption(weibo_user_signup);
            },
            error: function (data) {
                console.log('error')
            }
        });
    }
);
