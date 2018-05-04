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
            $("#keyword").text(user_info['introduction']);
        },
        error: function (data) {
            console.log('error')
        }
    });
}
getUserInfo();