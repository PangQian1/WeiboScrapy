weibo_user_sex_verify = {
    title: {
        text: '微博粉丝用户性别、认证分布情况',
        subtext: '微博爬虫统计',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data: ['男', '女', '微博认证', '未认证']
    },
    series: [
        {
            name: '认证统计',
            type: 'pie',
            selectedMode: 'single',
            radius: [0, '30%'],

            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data: [
                {value: 335, name: '微博认证', selected: true},
                {value: 679, name: '未认证'}
            ]
        },
        {
            name: '性别统计',
            type: 'pie',
            radius: ['40%', '55%'],
            label: {
                normal: {
                    formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                    backgroundColor: '#eee',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    borderRadius: 4,
                    padding: [0, 7],
                    rich: {
                        a: {
                            color: '#999',
                            lineHeight: 22,
                            align: 'center'
                        },
                        hr: {
                            borderColor: '#aaa',
                            width: '100%',
                            borderWidth: 0.5,
                            height: 0
                        },
                        b: {
                            fontSize: 16,
                            lineHeight: 33
                        },
                        per: {
                            color: '#eee',
                            backgroundColor: '#334455',
                            padding: [2, 4],
                            borderRadius: 2
                        }
                    }
                }
            },
            data: [
                {value: 335, name: '男'},
                {value: 310, name: '女'},
                {value: 234, name: '其他'}
            ]
        }
    ]
};

$("#bt_weibo_user_sex_verify").click(
    function () {
        $(".user_info").hide();
        $("#weibo_user_sex_verify").show();
        var chart = echarts.init(document.getElementById('weibo_user_sex_verify'));
        var ucid = GetUrlParam('ucid');
        $.ajax({
            type: 'get',
            url: API_HOST + '/api/user/sex_verify?ucid=' + ucid,
            data: '',
            dataType: 'json',
            success: function (data) {
                weibo_user_sex_verify.series[0].data = data['verify_list'];
                weibo_user_sex_verify.series[1].data = data['sex_list'];

                chart.setOption(weibo_user_sex_verify);
            },
            error: function (data) {
                console.log('error')
            }
        });
    }
);
