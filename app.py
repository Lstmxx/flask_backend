from flask import request, jsonify, g, session, make_response
from functools import wraps
import click
from init import app, db
from models import Article, User, ArticleTag
from toJosn import JSONHelper
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time
import os

token_generator = Serializer(app.config['SECRET_KEY'], expires_in=3600)


def create_token():
    pass

def verify_token(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        response = {
            'data': '',
            'message': '',
            'status': 200
        }
        print(request.headers)
        print(f"token is: {request.headers.get('Token')}")
        token = request.headers.get('Token')
        if token:
            try:
                data = token_generator.loads(token)
            except:
                response = {
                    'data': '',
                    'status': 403,
                    'message': '重新登陆啦靓仔'
                }
                return jsonify(response)
            if data['tokenType']:
                return func(*args, **kwargs)
            else:
                response = {
                    'data': '',
                    'status': 401,
                    'message': '假token要不得'
                }
                return jsonify(response)
        else:
            response = {
                'data': '',
                'status': 401,
                'message': '没有权限访问接口'
            }
            return jsonify(response)
    return wrap_func


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.route('/api/article/detail/<article_id>', methods=['GET'])
@verify_token
def load_article_detail(article_id):
    print(article_id)
    response = {
        'data': 'hello Flask',
        'status': 200
    }
    return jsonify(response)

@app.route('/api/article/list', methods=['GET'])
@verify_token
def load_article_list():
    response = {
        'data': 'hello Flask',
        'status': 200
    }
    return jsonify(response)

@app.route('/api/get-token', methods=['POST'])
def get_token():
    response = {
        'data': {
            'token': ''
        },
        'status': 200,
        'message': 'GET TOKEN SUCCESS'
    }
    print(request.headers)
    token = None
    if request.headers.get('Token'):
        try:
            data = token_generator.loads(request.headers.get('Token'))
            print(data)
        except:
            token = token_generator.dumps({
                'tokenType': 'visitor'
            }).decode('utf-8')
    else:
        token = token_generator.dumps({
            'tokenType': 'visitor'
        }).decode('utf-8')
    response['data']['token'] = token
    return jsonify(response)

@app.route('/api/tag/list', methods=['GET'])
@verify_token
def get_tag_list():
    response = {
        'data': {
            'tagList': ''
        },
        'status': 200,
        'message': 'success'
    }
    tag_list = ArticleTag.query.all()
    response['data']['tagList'] = JSONHelper.to_json_list(tag_list)
    return jsonify(response)

@app.route('/api/user-info', methods=['POST'])
@verify_token
def get_user_info():
    response = {
        'data': {
            'userInfo': ''
        },
        'status': 200,
        'message': 'success'
    }
    token = request.headers.get('Token')
    data = token_generator.loads(token)
    if data['tokenType'] == 'user':
        userId = data['userId']
        print(userId)
        user = User.query.get(userId)
        if user:
            response['data']['userInfo'] = {
                'name': user.username
            }
    return jsonify(response)

@app.route('/api/article/save', methods=['POST'])
@verify_token
def save_article():
    response = {
        'data': {
            'article': ''
        },
        'status': 200,
        'message': 'SAVE SUCCESS'
    }
    token = request.headers.get('Token')
    try:
        data = token_generator.loads(token)
    except:
        response = {
            'data': '',
            'status': 403,
            'message': '重新登陆啦靓仔'
        }
        return jsonify(response)
    if data['tokenType'] == 'user':
        userId = data['userId']
        values = request.get_json()
        required = ['article']
        if not all(k in values for k in required):
            response = {
                'data': '',
                'status': 500,
                'message': '文章都没有点保存啊'
            }
            return jsonify(response)
        Article

@app.route('/api/up-load', methods=['post'])
def save_up_load_file():
    upLoadFile = request.files['image']
    print(upLoadFile.filename)
    print(type(upLoadFile))
    filename = upLoadFile.filename
    if os.path.exists(f'media/{filename}'):
        filenames = filename.split('.')
        filename = filenames[0] + f'({time.time()}).' + filenames[1]
    with open(f'media/{filename}', 'wb') as f:
        f.write(upLoadFile.stream.read())
    response = {
        'data': {
            'imageName': filename
        },
        'message': '保存成功',
        'status': 200
    }
    return jsonify(response)

@app.route('/api/login', methods=['POST'])
def login():
    response = {
        'data': '',
        'message': '',
        'status': 0
    }
    values = request.get_json()
    required = ['password', 'username']
    if not all(k in values for k in required):
        print(request.headers)
    else:
        user = User.query.filter_by(username=values['username']).first()
        if user:
            if user.password == values['password']:
                response['message'] = 'login success'
                response['status'] = 200
                token = token_generator.dumps({
                    'tokenType': 'user',
                    "userId": user.id,
                    'iat': time.time()
                }).decode('utf-8')
                response['data'] = {
                    'token': token,
                    'userName': user.username
                }
            else:
                response['message'] = 'password incorrect'
                response['status'] = 200
        else:
            response['message'] = f"{values['username']} is no exist"
            response['status'] = 200
    print(response)
    return jsonify(response)

@app.route('/api/register', methods=['POST'])
def register():
    response = {
        'data': '',
        'message': '',
        'status': 0
    }
    values = request.get_json()
    required = ['password', 'username']
    if not all(k in values for k in required):
        response['message'] = 'register fail'
        response['status'] = 200
    else:
        has_user = User.query.filter_by(username=values['username']).count()
        if has_user == 0:
            user = User(username=values['username'], password=values['password'])
            db.session.add(user)
            db.session.commit()
            response['message'] = 'register success'
            response['status'] = 200
        else:
            response['message'] = f"{values['username']} is exist"
            response['status'] = 200
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)
