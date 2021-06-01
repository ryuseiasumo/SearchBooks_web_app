# from flask import Blueprint, render_template
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Aozora, SearchHistory
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

#ログイン後ページ
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

#検索ページ
@main.route('/search_books')
@login_required
def search_books():
    return render_template('search_books.html', name=current_user.name)

# @main.route('/search_books', methods=['POST']) #検索だからGET??
@main.route('/search_books', methods=['GET', 'POST']) #検索だからGET??
@login_required
def search_books_get():
    title_keyword = request.form.get('book_keyword')
    title_button = request.form.get('title_keyword_botton') #ボタンを押された方は空文字を返し、押されてない方はNoneを返す
    author_keyword = request.form.get('author_keyword')
    author_button = request.form.get('author_keyword_botton')

    #ユーザ情報取得
    from flask_login import current_user
    user_login_id = current_user.user_login_id #ユーザのID
    user_name = current_user.name

    #動作確認
    # print(db.session.query(SearchHistory.id, SearchHistory.user_login_id, SearchHistory.user_name, SearchHistory.search_word, SearchHistory.search_word_cnt).all())

    #タイトル検索
    if title_keyword and title_button != None:
        search = "%{}%".format(title_keyword)
        books = Aozora.query.filter(Aozora.title.like(search)).all() #ヒットしたリスト
        books_list = []
        for book in books:
            books_list.append([book.id, book.book_id, book.title, book.author, book.shuroku, book.publisher])
        # print(books_list)
        #動作確認
        # for book in books:
        #     print("{} - {}".format(book.id, book.title))
        # print("タイトル検索")

        #検索履歴データベースにサーチワードとユーザを入力
        search_data = SearchHistory.query.filter(SearchHistory.user_login_id==user_login_id, SearchHistory.search_word==title_keyword).first()

        if search_data: #すでにそのユーザで検索されたことがある場合
            search_data.search_word_cnt += 1 #データのカウントを更新(1追加)
            db.session.commit()

        else:
            #データの追加
            new_search_data = SearchHistory(user_login_id=user_login_id, user_name=user_name, search_word=title_keyword, search_word_cnt=1)
            db.session.add(new_search_data)
            db.session.commit()

        #検索結果のページ
        return render_template('search_result.html', name=current_user.name, books = books_list)

    #著者検索
    elif author_keyword and author_button != None:
        search = "%{}%".format(author_keyword)
        books = Aozora.query.filter(Aozora.author.like(search)).all()
        books_list = []
        for book in books:
            books_list.append([book.id, book.book_id, book.title, book.author, book.shuroku, book.publisher])
        #動作確認
        # for book in books:
        #     print("{} - {}".format(book.id, book.author))
        # print("著者検索")

        #検索履歴データベースにサーチワードとユーザを入力
        search_data = SearchHistory.query.filter(SearchHistory.user_login_id==user_login_id, SearchHistory.search_word==author_keyword).first()

        if search_data: #すでにそのユーザで検索されたことがある場合
            search_data.search_word_cnt += 1 #データのカウントを更新(1追加)
            db.session.commit()
            # return redirect(url_for('main.search_result', name=current_user.name, books = books))
        else:
        #データの追加
            new_search_data = SearchHistory(user_login_id=user_login_id, user_name=user_name, search_word=author_keyword, search_word_cnt=1)
            db.session.add(new_search_data)
            db.session.commit()
        #検索結果のページ
        return render_template('search_result.html', name=current_user.name, books = books_list)


    #何も指定していない場合
    else:
        # print("検索なし")
        return redirect(url_for('main.search_books'))



#検索結果のページ
# @main.route('/search_result')
# @login_required
# def search_result():
#     return render_template('search_result.html', name=current_user.name, books = [])

#履歴
@main.route('/history')
@login_required
def history():
    #ユーザ情報取得
    from flask_login import current_user
    user_login_id = current_user.user_login_id #ユーザのID
    # user_name = current_user.name

    # search = "%{}%".format(user_login_id)
    histories = SearchHistory.query.filter(SearchHistory.user_login_id == user_login_id).all()
    histories_list = []
    for history in histories:
        histories_list.append([history.id, history.user_login_id, history.user_name, history.search_word, history.search_word_cnt])


    ranking_dict = {} #検索数ランキング算出用ディクショナリ
    histories_all = SearchHistory.query.all()
    for each_history in histories_all:
        # print([each_history.user_name, each_history.search_word, each_history.search_word_cnt])

        # 検索ワードがすでにランキング算出用ディクショナリに存在する場合
        if each_history.search_word in ranking_dict.keys():
            ranking_dict[each_history.search_word] += each_history.search_word_cnt

        # 検索ワードがまだランキング算出用ディクショナリに存在しない場合
        else:
            ranking_dict[each_history.search_word] = each_history.search_word_cnt

    #検索数ランキング算出用ディクショナリを、検索数が多い順にソート
    search_ranking_top30 = []
    ranking = 1
    for search_word, cnt in sorted(ranking_dict.items(), key=lambda x: -x[1]):
        search_ranking_top30.append([ranking, str(search_word),int(cnt)])
        ranking += 1
        if ranking > 30:
            break

    # print(search_ranking_top30)

    return render_template('history.html', name=current_user.name, histories = histories_list, search_ranking_top30 = search_ranking_top30)
