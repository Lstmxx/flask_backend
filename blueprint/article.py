from flask import request, jsonify, g, session, make_response, Blueprint
from models import Article, User, ArticleTag
from utils import verify_token, token_generator
from toJosn import JSONHelper
from init import db

article_bp = Blueprint('article', __name__)

@article_bp.route('/api/article/store', methods=['POST'])
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
        values = values['article']
        required = ['name', 'tagId', 'content']
        if not all(k in values for k in required):
            response = {
                'data': '',
                'status': 500,
                'message': '参数有问题'
            }
            return jsonify(response)
        user = User.query.get(userId)
        if user == None:
            response = {
                'data': '',
                'status': 500,
                'message': '没有此用户'
            }
            return jsonify(response)
        tag = ArticleTag.query.get(values['tagId'])
        if tag == None:
            response = {
                'data': '',
                'status': 500,
                'message': '没有这种文章标题'
            }
        if values['content'] == '':
            response = {
                'data': '',
                'status': 500,
                'message': '没有文章啊'
            }
        article = Article(
            name=values['name'],
            content=values['content'],
            tag_id=values['tagId'],
            user_id=userId
        )
        db.session.add(article)
        db.session.commit()
        return jsonify(response)

@article_bp.route('/api/article/detail/<article_id>', methods=['GET'])
@verify_token
def load_article_detail(article_id):
    print(article_id)
    response = {
        'data': 'hello Flask',
        'status': 200
    }
    return jsonify(response)

@article_bp.route('/api/article/list', methods=['GET'])
@verify_token
def load_article_list():
    response = {
        'data': 'hello Flask',
        'status': 200
    }
    return jsonify(response)

@article_bp.route('/api/tag/list', methods=['GET'])
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
