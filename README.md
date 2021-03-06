# 青空文庫の書籍検索アプリケーション
書籍検索Webアプリケーションです。
学部3年の学生実験で作成したものをflaskを用いてpythonで作り直しました。
ローカルで動かすオフラインWebアプリケーションです。

# 仕様
* ログイン認証
* キーワード検索機能による、タイトル検索と著者検索（部分一致で検索）
* 自分の検索履歴の表示
* みんながよく調べる人気検索ワードランキングの表示


# 開発環境
* python 3.7.10
* pandas 1.2.3
* flask 1.1.2
* flask-login 0.5.0
* flask-sqlalchemy 2.5.1

# Requirement
* python
* pandas
* flask
* flask-login
* flask-sqlalchemy

# Installation
## flask周りのインストール
### pip 
```bash
$ pip install Flask
$ pip install flask-login
$ pip install -U Flask-SQLAlchemy
```
### conda
```bash
$ conda install -c anaconda flask
$ conda install -c anaconda flask-login
$ conda install -c conda-forge flask-sqlalchemy
```

# 使用方法
```bash
$ git clone https://github.com/ryuseiasumo/SearchBooks_web_app.git
$ cd SearchBooks_web_app
$ export FLASK_APP=project
$ export FLASK_DEBUG=1
$ python make_db.py #データベースの作成、初期化
$ flask run
```

# Note
```bash
$ flask run
```
をすると, 以下のローカルホストのリンクが表示されるので、ここからWebアプリを利用して下さい．
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
