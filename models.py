from init import db
from datetime import datetime
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    content = db.Column(db.Text(length=(2**31)-1))
    tag_id = db.Column(db.Integer, db.ForeignKey('article_tag.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    articles = db.relationship('Article')
    
class ArticleTag(db.Model):
    __tablename__ = 'article_tag'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)