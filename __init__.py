from flask import Flask
from flask_oauth import OAuth
from app import settings
GOOGLE_CLIENT_ID = '601137007401-p4hgs58b11r0l6i21hv8qu8hjct3dfh4.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'aH-zOJhEtM_jAj0-sJpm6FFP'
# one of the Redirect URIs from Google APIs console

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.config.from_object('app.settings.Production')
app.debug = DEBUG
app.secret_key = SECRET_KEY

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=settings.Production.FACEBOOK_APP_ID,
    consumer_secret=settings.Production.FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
    )

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='RGCphMmTY2a2ktPpyoVNYI6UT',
    consumer_secret='s3EiYzCsYVF3y6rXFT414vu6XDJYGvK18E6lfHvlRZIEVTFkvp'
    )

google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email', 'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET)


from app import controllers_jy
