# 青空文庫
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


# 使用方法
```bash
$ git clone https://github.com/ryuseiasumo/SearchBooks_web_app.git
$ export FLASK_APP=project
$ export FLASK_DEBUG=1
$ python make_db.py #データベースの作成、初期化
$ flask run
```

# Note
```bash
$ flask run
```
をすると, 以下が表示されると思うので, http以下からブラウザでWebアプリを利用して下さい．
* Running on http://〇〇 (Press CTRL+C to quit)
