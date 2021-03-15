from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/name', methods=['GET', 'POST'])
def get_name():
    if request.method == 'POST':
        return 'hibana from POST'
    else:
        return 'hibana from GET'


@app.route('/age')
def get_age():
    return '17'


# 用户资料endpoint
@app.route('/userProfile', methods=['GET', 'POST'])
def get_profile():
    if request.method == 'GET':
        name = request.args.get('name', '')
        print(name, flush=True)
        if(name == 'hibana'):
            return dict(name='hibana from GET', age=17)
        else:
            return dict(name='坏猫猫 from GET', age=114514)
    elif request.method == 'POST':
        print(request.json, flush=True)
        print(request.form, flush=True)
        print(request.data, flush=True)
        name = request.form.get('name')
        age = request.form.get('age')
        if(name == 'hibana'):
            return dict(name='hibana from POST', age=17)
        else:
            return dict(name='懒狗 from POST', age=1919810)
        return '1'

