# -*- coding: utf-8 -*-
from flask import render_template, Flask, request, redirect, url_for, flash,g,make_response,session,jsonify
from sqlalchemy import desc
from app import app,db
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import ArticleForm, CommentForm, UserForm, UserLogin

from app.models import Article,Comment,User
import pusher

@app.before_request
def befor_request():
	g.user_name=None
	if 'user_id' in session:
		g.user_name=session['user_name']


@app.route('/', methods=['GET'])
def article_list():
	if 'user_id' in session:
		context={}
		context['article_list']=Article.query.order_by(desc(Article.date_created)).limit(2)
		return render_template('home.html', context=context, active_tab='article_list')
	else:
		return redirect(url_for('login'))


@app.route('/article/create/', methods=['GET','POST'])
def article_create():
	if 'user_id' in session:
		form=ArticleForm()

		if request.method =='GET':
			return render_template('article/create.html', active_tab='article_create', form=form)
		elif request.method=='POST':
			if form.validate_on_submit():

				article=Article(
					title=form.title.data,
					author=form.author.data,
					category=form.category.data,
					content=form.content.data,
					like=0
				)

				db.session.add(article)
				db.session.commit()

				flash(u'게시글을 작성하였습니다.','success')
				return redirect(url_for('article_list'))
			return render_template('article/create.html', active_tab='article_create', form=form)
	else:
		return redirect(url_for('login'))



@app.route('/user/join', methods=['GET','POST'])
def join():
	form=UserForm()

	if request.method =='GET':
		return render_template('user/join.html', active_tab='join', form=form)
	elif request.method=='POST':
		if form.validate_on_submit():
			if db.session.query(User).filter(User.email==form.email.data).count()>0:
				flash(u'이미 가입된 이메일입니다.','danger')
				return render_template('user/join.html', active_tab='join', form=form)
			else:
				user=User(
					email=form.email.data,
					password=generate_password_hash(form.password.data),
					name=form.name.data,
				)
				db.session.add(user)
				db.session.commit()

				flash(u'회원가입되었습니다.','success')
				return redirect(url_for('article_list'))
		return render_template('user/join.html', active_tab='join', form=form)

@app.route('/user/login', methods=['GET','POST'])
def login():
	form=UserLogin()

	if request.method =='GET':
		return render_template('user/login.html', active_tab='login', form=form)
	elif request.method=='POST':
		user=db.session.query(User).filter(User.email == form.email.data).first()
		if user:
			if check_password_hash(user.password,form.password.data):
				session['user_id']=form.email.data
				session['user_name']=user.name
				return redirect(url_for('article_list'))
			else:
				flash(u'비밀번호가 틀렸어.','danger')
				return render_template('user/login.html', active_tab='login', form=form)
		else:
			flash(u'이메일이 존재안해.','danger')
			return render_template('user/login.html', active_tab='login', form=form)
@app.route('/Logout')
def logout():
	session.clear()
	return redirect(url_for('login'))



@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
	article=Article.query.get(id)

	comments=article.comments.order_by(desc(Comment.date_created)).all()

	return render_template('article/detail.html', article=article, comments=comments)



@app.route('/comment/create/<int:article_id>', methods=['GET','POST'])
def comment_create(article_id):
	form=CommentForm()

	if request.method =='GET':
		return render_template('comment/create.html', form=form)
	elif request.method=='POST':
		if form.validate_on_submit():

			comment=Comment(
				author=form.author.data,
				email=form.email.data,
				content=form.content.data,
				password=form.password.data,
				article=Article.query.get(article_id),
				like=0
			)

			db.session.add(comment)
			db.session.commit()

			flash(u'댓글을 작성하였습니다.','success')
			return redirect(url_for('article_detail', id=article_id))
		return render_template('comment/create.html',  form=form)


@app.route('/article/update/<int:id>', methods=['GET','POST'])
def article_update(id):
	article=Article.query.get(id)
	form=ArticleForm(request.form, obj=article)
	if request.method=='GET':
		return render_template('article/update.html',  form=form)
	elif request.method=='POST':
		if form.validate_on_submit():
			form.populate_obj(article)
			db.session.commit()
			return redirect(url_for('article_detail', id=id))
		return render_template('article/update.html', form=form)


	return render_template('article/update.html', form=form)

@app.route('/article/delete/<int:id>',methods=['GET','POST'])
def article_delete(id):
	if request.method=='GET':
		return render_template('article/delete.html', article_id=id)
	elif request.method=='POST':
		article_id=request.form['article_id']
		article=Article.query.get(article_id)
		db.session.delete(article)
		db.session.commit()
		flash(u'게시글을 삭제하였습니다.', 'success')
		return redirect(url_for('article_list'))


@app.route('/comment/like<int:id>/<int:id2>',methods=['GET','POST'])
def comment_like(id,id2):
	comment=Comment.query.get(id)
	comment.like+=1
	db.session.commit()
	article_id=id2

	return redirect(url_for('article_detail', id=article_id))


@app.route('/comment/delete<int:id>/<int:id2>',methods=['GET','POST'])
def comment_delete(id,id2):
	comment=Comment.query.get(id)

	db.session.delete(comment)
	db.session.commit()
	article_id=id2
	return redirect(url_for('article_detail', id=article_id))


@app.route('/comment/delete2<int:id>/<int:id2>',methods=['GET','POST'])
def comment_delete2(id,id2):
	comment=Comment.query.get(id)
	article_id=id2
	if request.method=='POST':
		password=request.form.get('text')	
		if comment.password==password: 
			db.session.delete(comment)
			db.session.commit()
			article_id=id2
			return redirect(url_for('article_detail', id=article_id))
		return redirect(url_for('article_detail', id=article_id))
	return redirect(url_for('article_detail', id=article_id))



@app.route('/article/like<int:id>',methods=['GET','POST'])
def article_like(id):
	article=Article.query.get(id)
	article.like+=1
	db.session.commit()
	return redirect(url_for('article_list'))


@app.route('/chatting' , methods=['GET','POST'])
def chatting():
	if 'user_id' in session:
		if request.method=='GET':
			return render_template('chatting.html' ,active_tab='chatting')
		elif request.method=='POST':
			name=session['user_name']
			msg=request.form.get("msg_data")
			p = pusher.Pusher(
			app_id='86080',
			key='057642e7dccfaba2eed4',
			secret='25fa99b0dcd5b99d607c'
			)
			p['test_channel'].trigger('my_event', {
				"name":name,
				"msg":msg
				})
			return ""
	else:
		return redirect(url_for('login'))




@app.route('/ajax/article_count')
def article_count():
	count = db.session.query(Article).count()
	return jsonify(count=count)

@app.route('/ajax/article_more')
def article_more():
	current_row=int(request.args.get('current_row'))
	row=int(request.args.get('count'))

	more_data=db.session.query(Article).order_by(desc(Article.date_created))[current_row:current_row+2]

	resp={}
	resp["data"]=[]
	temp={}
	for article in more_data:
		temp['id']=article.id
		temp['title']=article.title
		temp['content']=article.content
		temp['author']=article.author
		temp['category']=article.category
		temp['date_created']=article.date_created

		resp["data"].append(temp)
		temp={}
	return jsonify(resp)