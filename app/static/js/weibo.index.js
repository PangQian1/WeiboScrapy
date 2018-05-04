//绑定回车事件
$('#search_key').bind('keyup', function(event) {
　　if (event.keyCode == "13") {
　　　　 searchUser();
　　}
});

$("#search_btn").click(
    function () {
        searchUser();
    }
)
searchUser();

//搜索用户
function searchUser() {
    var username = $("#search_key").val();
    console.log(username);
    $.ajax({
        type: 'get',
        url: API_HOST + '/api/search/user?username=' + username,
        data: '',
        dataType: 'json',
        success: function (data) {
            var search_list = data['search_list'];
            var commend_list = data['commend_list'];
            $("#search_list").hide();
            $("#search_user_list").empty();
            for (key in search_list) {
                $("#search_list").show();
                var user_cell = getUserCell(search_list[key]);
                $("#search_user_list").append(user_cell);
            }

            $("#commend_list").hide();
            $("#commend_user_list").empty();
            for (var index in commend_list) {
                $("#commend_list").show();
                var user_cell_commend = getUserCell(commend_list[index]);
                $("#commend_user_list").append(user_cell_commend);
            }
        },
        error: function (data) {
            console.log('error')
        }
    });
}

// 获取单个用户样式
function getUserCell(user_info) {
    var user_title = user_info.name + " " + getSex(user_info.sex) + " →";
    var user_main_url = USER_MAIN_URL + '?ucid=' + user_info.ucid;
    var user_cell = "<div class=\"user_cell\"><h3 class=\"user_cell_title\"><a href=\" "
        + user_main_url + "\">"
        + user_title
        + "</a></h3><div class=\"user_cell_content\">"
        + user_info.introduction
        + "</div></div>";

    return user_cell;
}

// 性别处理
function getSex(sex) {
    var result = '女';
    if (sex == 'm')
        result = '男';
    return result;
}

