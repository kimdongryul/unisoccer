from datetime import timedelta


class Config(object):
    SECRET_KEY = "fuckyou"
    debug = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=3)


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "whddud2778@gmail.com"
    SQLALCHEMY_DATABASE_URI = "mysql+gaerdbms:///flaskr?instance=unisoccerteam:unisoccer-instance"
    migration_directory = "migrations"
