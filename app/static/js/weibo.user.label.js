
function showLabel(data){

    var label_table_head = "<div style=\"text-align: center;\">" +
        "<div class='row'>"+
        "<div style=\"width: 70%;margin-left: 15%\" class=\"col-xs-12\">" +
        "<table id=\"simple-table\" class=\"table table-striped table-bordered table-hover\">\n" +
        "<thead>"+
                "<tr style='background-color: darkgray' >"+
                    "<th style='text-align: center' class=\"hidden-480\">标签</th>"+
                    "<th style='text-align: center' class=\"hidden-480\">人数</th>"+
                    "<th style='text-align: center' class=\"hidden-480\">百分比</th>"+
                "</tr>"+
            "</thead>"+
            "<tbody id=\"pvBody\">"

    var label_tabel_tail = "</body>" +
        "</table>" +
        "</div>" +
        "</div></div>";

    var label_table_body = "";
    for(var i = 0; i < data['label'].length;
        i++){
        label_table_body += (
        "<tr>" +
        "<td>" + data['label'][i] + "</td>" +
        "<td>" + data['num'][i] + "</td>" +
        "<td>" + data['percentage'][i] + "</td>" +
        "</tr>")
    }

    var label_table = label_table_head + label_table_body + label_tabel_tail;

    return label_table;
}


$("#bt_weibo_user_label").click(
    function () {

        $(".user_info").hide();
        $("#weibo_user_label").show();
        //var chart = echarts.init(document.getElementById('weibo_user_sex_verify'));
        var ucid = GetUrlParam('ucid');

        $.ajax({
            type: 'get',
            url: API_HOST + '/api/user/label?ucid=' + ucid,
            data: '',
            dataType: 'json',
            success: function (data) {
                console.log(data)
                var res = showLabel(data);
                console.log(res);
                $("#weibo_user_label").append(res);
            },
            error: function (data) {
                console.log('error')
            }
        });


    }
);

