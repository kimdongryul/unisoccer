class Config(object):
	SECRET_KEY="abcdefg"
	debug= False

class Production(Config):
	debug=True
	CSRF_ENABLED = False
	ADMIN = "jhdr1080@gmail.com"
	SQLALCHEMY_DATABASE_URI="mysql+gaerdbms:///flaskr?instance=likelionryul:flaskr-instance"
	migration_directory="migrations"
	