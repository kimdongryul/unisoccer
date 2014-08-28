# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, g, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from app import app, db
from app.forms import ArticleForm, CommentForm, UserForm, LoginForm
from app.models import Article, Comment, User


@app.before_request
def before_request():
    g.user_name = None
    if 'user_name' in session:
        g.user_name = session['user_name']


@app.route('/')
def article_list():
    context = {}

    context['article_list'] = Article.query.order_by(
        desc(Article.date_created)).limit(2)

    return render_template('home.html', context=context, active_tab='article_list')


@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    if g.user_name == None:
        flash(u'로그인 후 이용하세요.', 'danger')
        return redirect(url_for('login'))
    else:
        form = ArticleForm()
        if request.method == 'GET':
            return render_template('article/create.html', form=form, active_tab='article_create')
        elif request.method == 'POST':
            if form.validate_on_submit():
                article = Article(
                    title=form.title.data,
                    author=form.author.data,
                    category=form.category.data,
                    content=form.content.data
                )
                db.session.add(article)
                db.session.commit()

                flash(u'게시글을 작성하였습니다.', 'success')
                return redirect(url_for('article_list'))
            return render_template('article/create.html', form=form, active_tab='article_create')


@app.route('/user/signup/', methods=["GET", "POST"])
def sign_up():
    form = UserForm()
    if request.method == 'GET':
        return render_template('user/signup.html', form=form, active_tab='sign_up')
    elif request.method == 'POST':
        if form.validate_on_submit():
            if db.session.query(User).filter(User.email == form.email.data).count() > 0:
                flash(u'이미 가입된 이메일입니다.', 'danger')
                return render_template('user/signup.html', form=form, active_tab='sign_up')
            else:
                user = User(
                    email=form.email.data,
                    password=generate_password_hash(form.password.data),
                    name=form.name.data
                )

                db.session.add(user)
                db.session.commit()

                flash(u'회원가입을 완료하였습니다.', 'success')
                return redirect(url_for('article_list'))

        return render_template('user/signup.html', form=form, active_tab='sign_up')


@app.route('/user/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('user/login.html', form=form, active_tab='log_in')
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User).filter(
                User.email == form.email.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    session['user_name'] = user.name
                    flash(u'로그인 하였습니다.', 'success')
                    return redirect(url_for('article_list'))
                else:
                    flash(u'비밀번호가 틀렸습니다. 다시 로그인 해 주세요.', 'danger')
                    return render_template('user/login.html', form=form, active_tab='log_in')
            else:
                flash(u'이메일 주소가 없습니다. 다시 로그인 해 주세요.', 'danger')
                return render_template('user/login.html', form=form, active_tab='log_in')
        return render_template('user/login.html', form=form, active_tab='log_in')


@app.route('/user/logout/', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('article_list'))


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    article = Article.query.get(id)

    comments = article.comments.order_by(desc(Comment.date_created)).all()

    return render_template('article/detail.html', article=article, comments=comments)


@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    form = CommentForm()
    if request.method == 'GET':
        return render_template('comment/create.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(
                author=form.author.data,
                email=form.email.data,
                content=form.content.data,
                password=form.password.data,
                article=Article.query.get(article_id)
            )
            db.session.add(comment)
            db.session.commit()

            flash(u'게시글을 작성하였습니다.', 'success')
            return redirect(url_for('article_detail', id=article_id))
        return render_template('comment/create.html', form=form)


@app.route('/article/detail/<int:article_id>/<int:comment_id>')
def comment_like(article_id, comment_id):
    comment = Comment.query.get(comment_id)
    comment.like = comment.like + 1
    db.session.commit()
    return redirect(url_for('article_detail', id=article_id))


@app.route('/comment/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    form = ArticleForm(request.form, obj=article)
    if request.method == 'GET':
        return render_template('article/update.html', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(article)
            db.session.commit()
            return redirect(url_for('article_detail', id=id))
        return render_template('article/update.html', form=form)


@app.route('/comment/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'GET':
        return render_template('article/detail.html', article_id=id)
    elif request.method == 'POST':
        article_id = request.form.get('article_id')
        article = Article.query.get(article_id)
        db.session.delete(article)
        db.session.commit()

        flash(u'게시글을 삭제하였습니다.', 'success')
        return redirect(url_for('article_list'))


@app.route('/comment/delete/<int:article_id>/<int:comment_id>', methods=['GET', 'POST'])
def comment_delete(article_id, comment_id):
    article = Article.query.get(article_id)
    comment = Comment.query.get(comment_id)
    if request.method == 'GET':
        return render_template('article/detail.html', article=article, comments=comment)
    elif request.method == 'POST':
        if comment.password == request.form.get('password'):
            db.session.delete(comment)
            db.session.commit()
            return redirect(url_for('article_detail', id=article_id))
        else:
            return render_template('article/detail.html', article=article, comments=comment)
    else:
        return render_template('article/detail.html', article=article, comments=comment)


@app.route('/ajax/article_count')
def article_count():
    count = db.session.query(Article).count()
    return jsonify(count=count)


@app.route('/ajax/article_more')
def article_more():
    current_row = int(request.args.get('current_row'))
    row = int(request.args.get('count'))

    more_data = db.session.query(Article).order_by(
        desc(Article.date_created)).offset(current_row).limit(2)

    resp = {}
    resp["data"] = []
    temp = {}
    for article in more_data:
        temp['id'] = article.id
        temp['title'] = article.title
        temp['content'] = article.content
        temp['author'] = article.author
        temp['category'] = article.category
        temp['date_created'] = article.date_created
        resp['data'].append(temp)
        temp = {}

    return jsonify(resp)
