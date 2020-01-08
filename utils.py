from flask import request, jsonify, g, session, make_response
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from init import app
from toJosn import JSONHelper

token_generator = Serializer(app.config['SECRET_KEY'], expires_in=3600)

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