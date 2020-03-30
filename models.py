from init import db
from datetime import datetime
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index = True)
    content = db.Column(db.Text(length=(2**31)-1))
    description = db.Column(db.Text(length=(2**31)-1))
    tag_id = db.Column(db.Integer, db.ForeignKey('article_tag.id'), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow, index = True)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index = True)
    avatar_image = db.Column(db.String(64), index = True)
    like_num = db.Column(db.Integer, default = 0)
    watch_num = db.Column(db.Integer, default = 0)
    comment = db.relationship('Comment', cascade = 'delete')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True)
    password = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    articles = db.relationship('Article')
    avatar_image = db.Column(db.String(64))
    root_id = db.Column(db.Integer, db.ForeignKey('authorization.id'), index = True)
    
class Authorization(db.Model):
    __tablename__ = 'authorization'
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow, index = True)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index = True)
    name = db.Column(db.String(64))
    root = db.Column(db.Integer)

class ArticleTag(db.Model):
    __tablename__ = 'article_tag'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64))
    tag_color = db.Column(db.String(64))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow, index = True)
    update_time = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow, index = True)

class LikeRecord(db.Model):
    __tablename__ = 'like_record'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), index = True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow, index = True)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index = True)

class WatchRecord(db.Model):
    __tablename__ = 'watch_record'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), index = True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow, index = True)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index = True)