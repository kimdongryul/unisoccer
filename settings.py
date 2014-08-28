class Config(object):
    SECRET_KEY = 'sldkjflksjdlfk'
    FACEBOOK_APP_ID = '374949859324987'
    FACEBOOK_APP_SECRET = '32daa7cd70c2e3e2bfac04c635bf5b97'
    debug = False


class Production(Config):
    debug = True
