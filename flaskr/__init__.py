import os

from flask import Flask
from flask import request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import db
    db.init_app(app)

    def query_db(query, args=(), one=False):
        cur = db.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

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

    ## 用户资料endpoint
    # R: Read 读取创建的user profile\GET
    # C: Create 创建一个user profile\POST
    # U: Update 更新创建的user profile\PUT
    # D: Delete 删除创建的user profile\DELETE

    @app.route('/userProfile', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def userProfile():
        if request.method == 'GET':
            # name = request.args.get('name', '')
            uid = request.args.get('uid', 1)
            # print(name, flush=True)
            print(uid, flush=True)
            # 3. 写sql
            query = "SELECT *FROM userProfile WHERE id={}".format(uid)
            print(query, flush=True)
            # 通过用户的id来查询用户的资料
            result = query_db(query, one=True)
            # 1. 获取数据库连接
            # connection = db.get_db()
            # 2. 获取一个数据库的游标 cursor
            # 4. 执行sql
            # cursor = connection.execute(query)
            # result = cursor.fetchall()
            print(result, flush=True)
            if result is None:
                return dict(message="404 not found")
            else:
                name = result['name']
                age = result['age']
                print(result['name'])
                print(result['age'])
                return dict(name=name, age=age)
            # cursor.close()
            # 5. 处理从数据库里读取的数据
            # 6. 将数据返回给调用者
            return '1'

            # 从数据库里读取
            # if (name == 'hibana'):
            #     return dict(name='hibana from GET', age=17)
            # else:
            #     return dict(name='屑学弟 from GET', age=114514)
        elif request.method == 'POST':
            # name
            # fans
            print(request.json, flush=True)
            # print(request.form, flush=True)
            # print(request.data, flush=True)
            # name = request.form.get('name')
            # age = request.form.get('age')
            name = request.json.get('name')
            age = request.json.get('age')
            # 获取post body中的name和fans
            # 输入新的数据到数据库
            # 1.获取新的数据库连接
            connection = db.get_db()
            # 写sql
            query = "INSERT INTO userProfile (name, age) values('{}', {})".format(name, age)
            print(query)
            # 2.执行
            try:
                cursor = connection.execute(query)
                # 3.DML Data Manipulate Language
                # 当你对数据库里面的数据有改动的时候，需要commit，否则改动不会生效
                # execute的时候就会去数据库里面执行这条sql，如果有错误，会报错
                connection.commit()

                print(cursor.lastrowid)
                return dict(success=True)
            except:
                return dict(success=False, message="username exist", errorCode=1)
            #
            #             if (name == 'hibana'):
            #     return dict(name='hibana from POST', age=17)
            # else:
            #     return dict(name='懒狗 from POST', age=1919810)
            # return '1'
        elif request.method == 'PUT':
            print(request.json, flush=True)
            uid = request.args.get('uid', 1)
            name = request.json.get('name')
            age = request.json.get('age')
            connection = db.get_db()
            query = "UPDATE userProfile SET name = '{}', age = {} WHERE id = {}".format(name, age, uid)
            print(query)
            try:
                cursor = connection.execute(query)
                connection.commit()
                print(cursor.lastrowid)
                return dict(success=True)
            except:
                return dict(success=False, message="username already existed", errorCode=1)
            return 1
        elif request.method == 'DELETE':
            uid = request.args.get('uid', 1)
            connection = db.get_db()
            query = "DELETE from userProfile WHERE id = {}".format(uid)
            connection.execute(query)
            connection.commit()
            return dict(success=True)

    return app
