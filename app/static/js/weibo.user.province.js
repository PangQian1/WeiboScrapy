function randomData() {
    return Math.round(Math.random() * 1000);
}

weibo_user_province = {
    title: {
        text: '微博用户地区分布数量统计图',
        subtext: '微博爬虫统计',
        left: 'center'
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ['微博用户数量']
    },
    visualMap: {
        min: 0,
        max: 10,
        left: 'left',
        top: 'bottom',
        text: ['高', '低'],           // 文本，默认为数值文本
        inRange: {
            color: ['#e0ffff', '#006edd']
        },
        calculable: true
    },
    toolbox: {
        show: true,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
            dataView: {readOnly: false},
            restore: {},
            saveAsImage: {}
        }
    },
    series: [
        {
            name: '微博用户数量',
            type: 'map',
            mapType: 'china',
            label: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            data: [
                {name: '北京', value: randomData()},
                {name: '天津', value: randomData()},
                {name: '上海', value: randomData()},
                {name: '重庆', value: randomData()},
                {name: '河北', value: randomData()},
                {name: '安徽', value: randomData()},
                {name: '新疆', value: randomData()},
                {name: '浙江', value: randomData()},
                {name: '江西', value: randomData()},
                {name: '山西', value: randomData()},
                {name: '内蒙古', value: randomData()},
                {name: '吉林', value: randomData()},
                {name: '福建', value: randomData()},
                {name: '广东', value: randomData()},
                {name: '西藏', value: randomData()},
                {name: '四川', value: randomData()},
                {name: '宁夏', value: randomData()},
                {name: '香港', value: randomData()},
                {name: '澳门', value: randomData()}
            ]
        },
    ]
};

function showChina() {
    $(".user_info").hide();
    $("#weibo_user_china").show();
    var chart = echarts.init(document.getElementById('weibo_user_china'));
    var ucid = GetUrlParam('ucid');
    $.ajax({
        type: 'get',
        url: 'http://127.0.0.1:5000/user/province/list?ucid=' + ucid,
        data: '',
        dataType: 'json',
        success: function (data) {
            console.log(data['china_list']);

            weibo_user_province.series[0].data = data['china_list'];
            chart.setOption(weibo_user_province);
        },
        error: function (data) {
            console.log('error')
        }
    });
}
showChina();

$("#bt_weibo_user_china").click(
    function () {
        showChina()
    }
);


