from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html') #ログインページ

@auth.route('/login', methods=['POST'])
def login_post():
    user_login_id = request.form.get('user_login_id')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(user_login_id=user_login_id).first()

    # ユーザが存在するかチェック
    # ユーザが入力したパスワードをハッシュ化し，データベース内のハッシュ化されたパスワードと比較する
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) #存在しないもしくはパスワードが違う場合、ログインページをリロード

    #ログイン
    login_user(user, remember=remember) #ユーザーローダー（セッションクッキーに保存されているIDからユーザーを見つける）
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    user_login_id = request.form.get('user_login_id')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(user_login_id=user_login_id).first() # if this returns a user, then the user_login_id already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('This User ID already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(user_login_id=user_login_id, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
