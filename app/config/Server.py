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
    user_controller    = UserController.UserController()
    user_province_list = user_controller.userProvinceList()

    return render(user_province_list)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True)