/**
 * 获取用户的个人信息
 */
function getUserInfo() {
    ucid = GetUrlParam('ucid');

    $.ajax({
        type: 'get',
        url: API_HOST + '/api/user/info?ucid=' + ucid,
        data: '',
        dataType: 'json',
        success: function (data) {
            user_info = data;
            $("#title").text(user_info['name']);
            $("#introduction").text(user_info['introduction']);
            $("#sex").text(getSex(user_info['sex']));
            $("#verify").text(getVerify(user_info['is_verify']));
            if (user_info['keywords'].length > 0) {
                $("#keywords").text('KeyWords: ' + user_info['keywords']);
            } else {
                $("#keywords").text('KeyWords: 本宝宝暂时没有关键词~');
            }
            $("#follow_number").text('关注:' + user_info['follow_number']);
            $("#follower_number").text('粉丝:' + user_info['follower_number']);
            $("#weibo_number").text('微博:' + user_info['weibo_number']);
        },
        error: function (data) {
            console.log('error')
        }
    });
}
getUserInfo();

$("#title").mouseover(function () {
    $("#user_info").show();
});

$("#title").mouseout(function () {
    $("#user_info").hide();
});