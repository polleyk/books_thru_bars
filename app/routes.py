from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.get_data import get_ithaca, retrieve_facilities, retrieve_genres, retrieve_mailings
from app.login import get_user, check_password
from app.book_retrieve import get_all_titles, get_all_authors, get_all_editors, get_genres

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

@app.route('/what-we-do', methods=['GET', 'POST'])
def data():
    facilities = retrieve_facilities()
    ithaca = get_ithaca()
    library, sent = retrieve_genres()
    mailings = retrieve_mailings()

    return render_template('data.html', title="What We Do",
                           facilities=facilities, ithaca=ithaca, library=library, sent=sent, mailings=mailings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.username.data)

        if user is None or not check_password(user, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/library/log-in', methods=['POST', 'GET'])
def log_book_in():
    titles = get_all_titles()
    authors = get_all_authors()
    editors = get_all_editors()
    genres = get_genres()
    return render_template('bookin.html', books=titles, auths=authors, edits=editors, gens=genres)

@app.route('/submitbook', methods=['POST', 'GET'])
def submit_book():
    return "oops"

@app.route('/test', methods=['POST', 'GET'])
def test():
    return render_template('test.html')

@app.route('/autocomp', methods=['POST', 'GET'])
def ajaxautocomplete():
    if request.method == 'POST':
        return get_all_titles()
    else:
        return "oops"