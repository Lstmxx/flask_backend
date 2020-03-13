from flask import request, jsonify, g, session, make_response, Blueprint
from models import Article, User, ArticleTag
from utils import verify_token, token_generator
from toJosn import JSONHelper
from init import db

article_bp = Blueprint('article', __name__)

@article_bp.route('/api/article/store', methods=['POST'])
@verify_token
def save_article(tokenData):
    response = {
        'data': {
            'article': ''
        },
        'status': 200,
        'message': 'SAVE SUCCESS'
    }
    if tokenData['tokenType'] == 'user':
        userId = tokenData['userId']
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
    print(f'文章ID：{article_id}')
    values = request.get_json()
    response = {
        'data': 'hello Flask',
        'status': 200
    }
    return jsonify(response)

@article_bp.route('/api/article/list', methods=['GET'])
@verify_token
def load_article_list():
    response = {
        'data': '',
        'status': 500,
        'message': '参数错误'
    }
    values = request.get_json()
    require = ['page', 'pageSize']
    if not all(k in values for k in require):
        return jsonify(response)
    response = {
        'data': 'hello Flask',
        'status': 200
    }
    return jsonify(response)

@article_bp.route('/api/tag/list', methods=['GET'])
@verify_token
def get_tag_list(tokenData):
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
