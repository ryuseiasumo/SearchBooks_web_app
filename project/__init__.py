from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    #ユーザ-ローダーを指定（セッションクッキーに保存されているIDから特定のユーザーを見つける方法）
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # 主キーであるIDで検索
        return User.query.get(int(user_id))

    from .models import Aozora, SearchHistory

    # 認証部分用のblueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # 認証部分以外用のblueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
