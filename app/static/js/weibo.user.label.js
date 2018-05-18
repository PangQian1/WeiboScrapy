
function showLabel() {

    var label_table = ""

}


$("#bt_weibo_user_label").click(
    function () {

        $(".user_info").hide();
        $("#bt_weibo_user_label").show();
        //var chart = echarts.init(document.getElementById('weibo_user_sex_verify'));
        var ucid = GetUrlParam('ucid');


        $.ajax({
            type: 'get',
            url: API_HOST + '/api/user/label?ucid=' + ucid,
            data: '',
            dataType: 'json',
            success: function (data) {

            },
            error: function (data) {
                console.log('error')
            }
        });


    }
);

