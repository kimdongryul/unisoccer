from app import db

class Article(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(255))
	content=db.Column(db.Text())
	author=db.Column(db.String(255))
	category=db.Column(db.String(255))
	like=db.Column(db.Integer())
	date_created=db.Column(db.DateTime(), default=db.func.now())

class Comment(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	article_id=db.Column(db.Integer, db.ForeignKey('article.id'))
	article=db.relationship('Article', backref=db.backref('comments', cascade='all,delete-orphan', lazy='dynamic'))

	author=db.Column(db.String(255))
	email=db.Column(db.String(255))
	password=db.Column(db.String(255))
	content=db.Column(db.Text())
	like=db.Column(db.Integer())
	date_created=db.Column(db.DateTime(), default=db.func.now())

class User(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.String(255))
	password=db.Column(db.String(255))
	name=db.Column(db.String(255))
	join_date=db.Column(db.DateTime(), default=db.func.now())
