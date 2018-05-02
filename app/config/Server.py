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

@app.route('/user/province/list', methods=['GET', 'POST'])
def userProvinceList():
    ucid               = request.args.get('ucid', '')
    user_controller    = UserController.UserController()
    user_province_list = user_controller.userProvinceList(ucid)

    return render(user_province_list)

@app.route('/user/sex/verify', methods=['GET', 'POST'])
def userSexVerifyList():
    ucid               = request.args.get('ucid', '')
    user_controller    = UserController.UserController()
    user_sex_verify = user_controller.userSexVerifyList(ucid)

    return render(user_sex_verify)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True)