
//总页数
var page_count = 1;
//当前页码
var current_page = 1;
//每页大小
var page_size = 10;

function getLabel(data){
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

    return label_table_head + label_table_body + label_tabel_tail;
}

function getPage(total) {

    //前一頁
     var user_label_page_head = '<li class="paginate_button previous" aria-controls="dynamic-table" tabindex="0"' +
        'id="dynamic-table_previous" onclick="showLabels(' + ((current_page == 1) ? 1 : current_page - 1) +')">' +
        '<a href="#">Previous</a>' +
        '</li>';

     //页码初始化
     var page = 1;
     for(var i = 0; i < total; i += 10) {
        user_label_page_head += '<li class="paginate_button" aria-controls="dynamic-table" tabindex="0" onclick="showLabels(' + (page) +')"><a href="#">' + (page) + '</a></li>';
        page++;
     }
     page_count = page - 1;

     //后一页
     var user_label_page_tail = '<li class="paginate_button next" aria-controls="dynamic-table" tabindex="0" ' +
        'id="dynamic-table_next" onclick="showLabels(' + ((current_page == page_count) ? page_count : current_page + 1) +')">' +
        '<a href="#">Next</a>' +
        '</li>';

     //console.log(user_label_page_tail);

    user_label_page_head += user_label_page_tail;
    return user_label_page_head;
}

function showLabels(page) {

    console.log('aaa' + current_page);
    current_page = page;

    $(".user_info").hide();
    $("#weibo_user_label").show();
    var ucid = GetUrlParam('ucid');
    ucid = ucid.replace('#', '');

    console.log(page);
    console.log(page_size);

    url = API_HOST + '/api/user/label?ucid=' + ucid + '&page=' + page + '&page_size=' + page_size;

    $.ajax({
        type: 'get',
        url: url,
        data: '',
        dataType: 'json',
        success: function (data) {
            var label = getLabel(data);
            $("#weibo_user_label_content").empty();
            $("#weibo_user_label_content").append(label);

            var label_page = getPage(data['total']);
            $("#weibo_user_label_page").empty();
            $("#weibo_user_label_page").append(label_page);
        },
        error: function (data) {
            console.log('error')
        }
    });
}

$("#bt_weibo_user_label").click(
    function () {
        showLabels(1)
    }
);
