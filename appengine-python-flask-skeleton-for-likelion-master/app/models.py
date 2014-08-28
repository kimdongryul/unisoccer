from app import db

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	teamname = db.Column(db.String(255))
	location_first = db.Column(db.String(255))
	location_second= db.Column(db.String(255))
	university= db.Column(db.String(255))
	Introduce = db.Column(db.Text())
	
class Location_first(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location_first = db.Column(db.String(255))

class Location_second(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location_second = db.Column(db.String(255))
	