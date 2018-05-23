weibo_userInfo_statistics = {
    title: {
        text: '微博粉丝信息填写统计情况',
        subtext: '微博爬虫统计',
        left: 'center',
        top: '0'
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'line'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data:['填写人数', '未填写人数'],
        x: 'left',
        orient: 'horizontal'
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value'
        }
    ],
    yAxis : [
        {
            type : 'category',
            data : ['地区','生日','标签','注册时间','简介']
        }
    ],
    series : [
        {
            name:'填写人数',
            type:'bar',
            stack: '总量',
            barWidth: 50,
            itemStyle : { normal: {
                        label : {show: true, position: 'insideRight'}
                                }
                     },
            data:[320, 302, 301, 390, 330]
        },
        {
            name:'未填写人数',
            type:'bar',
            stack: '总量',
            barWidth: 50,
            itemStyle : { normal: {
                label : {show: true, position: 'insideRight'}}},
            data:[820, 832, 901, 1290, 1330]
        }
    ]
};


option = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data:['填写人数', '未填写人数']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value'
        }
    ],
    yAxis : [
        {
            type : 'category',
            data : ['地区','生日','标签','注册时间','简介']
        }
    ],
    series : [
        {
            name:'填写人数',
            type:'bar',
            stack: '总量',
            itemStyle : { normal: {label : {show: true, position: 'insideRight'}}},
            data:[320, 302, 301, 334, 390, 330, 320]
        },
        {
            name:'未填写人数',
            type:'bar',
            stack: '总量',
            itemStyle : { normal: {label : {show: true, position: 'insideRight'}}},
            data:[120, 132, 101, 134, 90, 230, 210]
        }
    ]
};



$("#bt_weibo_user_statistics").click(
    function () {
        $(".user_info").hide();
        $("#weibo_user_statistics").show();
        var chart = echarts.init(document.getElementById('weibo_user_statistics'));
        var ucid = GetUrlParam('ucid');
        $.ajax({
            type: 'get',
            url: API_HOST + '/api/user/statistics?ucid=' + ucid,
            data: '',
            dataType: 'json',
            success: function (data) {
                weibo_userInfo_statistics.series[0].data = data['complete_num'];
                weibo_userInfo_statistics.series[1].data = data['incomplete_num'];

                chart.setOption(weibo_userInfo_statistics);

                //option.series[0].data = data['complete_num'];
                //option.series[1].data = data['incomplete_num'];

                //chart.setOption(option);
            },
            error: function (data) {
                console.log('error')
            }
        });
    }
);