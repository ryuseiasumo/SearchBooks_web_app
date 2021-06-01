from flask_login import UserMixin #Flask-Loginの属性をモデルに追加
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # 主キー
    user_login_id = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Aozora(db.Model):
    __tablename__ = "aozora"
    id = db.Column(db.Integer, primary_key=True) # 主キー
    book_id = db.Column(db.Integer) # 主キー
    title = db.Column(db.String(200))
    author = db.Column(db.String(100))
    shuroku = db.Column(db.String(200))
    publisher = db.Column(db.String(200))



class SearchHistory(db.Model):
    __tablename__ = "search_history"
    id = db.Column(db.Integer, primary_key=True) # 主キー
    user_login_id = db.Column(db.String(100))
    user_name = db.Column(db.String(100))
    search_word = db.Column(db.String(200))
    search_word_cnt = db.Column(db.Integer)
