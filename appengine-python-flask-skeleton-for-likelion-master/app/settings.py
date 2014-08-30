
class Config(object):
    SECRET_KEY = 'sldkjflksjdlfk'
    FACEBOOK_APP_ID = '754223001285432'
    FACEBOOK_APP_SECRET = '3efb03300bcfaf56048ac87c2f758ac5'
    debug = False

class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "jhdr1080@gmail.com"
    SQLALCHEMY_DATABASE_URI = "mysql+gaerdbms:///flaskr?instance=likelionryul:flaskr-instance"
    migration_directory = "migrations"
