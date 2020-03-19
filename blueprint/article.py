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
        required = ['name', 'tagId', 'content', 'description']
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
                'message': '没有这种文章类型'
            }
        if values['content'] == '':
            response = {
                'data': '',
                'status': 500,
                'message': '没有文章啊'
            }
        description = ''
        article = Article(
            name = values['name'],
            content = values['content'],
            tag_id = values['tagId'],
            description = values['description'],
            user_id = userId
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

@article_bp.route('/api/article/page', methods=['POST'])
def load_article_page():
    response = {
        'data': '',
        'status': 500,
        'message': '参数错误'
    }
    values = request.get_json()
    require = ['page', 'pageSize']
    if not all(k in values for k in require):
        return jsonify(response)
    queryList = ['tag_id', 'name', 'create_time', 'avatar_image', 'watch_num', 'like_num', 'description']
    resList = db.session.query(Article.tag_id,
                                Article.name,
                                Article.create_time,
                                Article.avatar_image,
                                Article.watch_num,
                                Article.like_num,
                                Article.description).order_by(Article.create_time.desc()).all()
    articleList = []
    for res in resList:
        data = dict(map(lambda x, y: [x, y], queryList, res))
        articleList.append(data)
    print(articleList)
    response = {
        'data': {
            'articleList': articleList
        },
        'status': 200,
        'message': '成功'
    }
    return jsonify(response)

@article_bp.route('/api/tag/list', methods=['POST'])
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
