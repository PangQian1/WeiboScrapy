import json
from flask import Flask
from flask import request, make_response
from app.controller import UserController

app = Flask(__name__)
app.config['DEBUG']=True

def render(data):
    response = make_response(json.dumps(data))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

# 用户信息填写统计
@app.route('/api/user/statistics', methods=['GET', 'POST'])
def userInfoStatistics():

    ucid               = request.args.get('ucid', '')
    user_controller    = UserController.UserController()
    user_info_statistics = user_controller.userInfoStatistics(ucid)

    return render(user_info_statistics)


# 用户个人信息
@app.route('/api/user/info', methods=['GET', 'POST'])
def userInfo():

    ucid               = request.args.get('ucid', '')
    user_controller    = UserController.UserController()
    user_info = user_controller.userInfo(ucid)

    return render(user_info)

# 用户省份信息
@app.route('/api/user/province', methods=['GET', 'POST'])
def userProvinceList():
    ucid               = request.args.get('ucid', '')
    user_controller    = UserController.UserController()
    user_province_list = user_controller.userProvinceList(ucid)

    return render(user_province_list)

# 用户性别信息
@app.route('/api/user/sex_verify', methods=['GET', 'POST'])
def userSexVerifyList():

    ucid               = request.args.get('ucid', '')
    user_controller    = UserController.UserController()
    user_sex_verify = user_controller.userSexVerifyList(ucid)

    return render(user_sex_verify)

# 用户注册时间
@app.route('/api/user/signup_time', methods=['GET', 'POST'])
def userSignupList():

    ucid               = request.args.get('ucid', '')
    user_controller    = UserController.UserController()
    user_up_time = user_controller.userSignupList(ucid)

    return render(user_up_time)


# 用户标签
@app.route('/api/user/label', methods=['GET', 'POST'])
def userLabel():

    ucid            = request.args.get('ucid', '')
    page            = request.args.get('page', 1)
    page_size       = request.args.get('page_size', 10)
    user_controller = UserController.UserController()
    user_label = user_controller.userLabelList(ucid, int(page), int(page_size))

    return render(user_label)

# 搜索用户
@app.route('/api/search/user', methods=['GET', 'POST'])
def userSearchList():

    user_name       = request.args.get('username', '')
    user_controller = UserController.UserController()
    user_list = user_controller.userSearchList(user_name)

    return render(user_list)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True)