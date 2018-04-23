from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Flask!'

if __name__ == '__main__':
    app.run()

from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return 'Hello h!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'welcome/html')])
    return [b"Hello World"]