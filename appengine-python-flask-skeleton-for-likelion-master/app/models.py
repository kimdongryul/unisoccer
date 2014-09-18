from app import db

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	teamname = db.Column(db.String(255))
	location = db.Column(db.String(255))
	university= db.Column(db.String(255))
	Introduce = db.Column(db.Text())
	favorite_date = db.Column(db.String(255))
	favorite_place = db.Column(db.String(255))
	ranking_score= db.Column(db.Integer(), default=0)
	ranking_result= db.Column(db.String(255))
	leader_name= db.Column(db.String(255))


	
class Location_first(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.String(255))
	upper_id=db.Column(db.Integer(), default=0)

class University(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	university = db.Column(db.String(255))
	location_id=db.Column(db.Integer(), default=0)
	address=db.Column(db.Text())


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	team_id= db.Column(db.Integer, db.ForeignKey('team.id'))
	team = db.relationship('Team',backref=db.backref('users', cascade='all, delete-orphan', lazy='dynamic'))
	email = db.Column(db.String(255))
	name= db.Column(db.String(255))
	phone_number= db.Column(db.String(255))
	university= db.Column(db.String(255))
	# facebook_id=
