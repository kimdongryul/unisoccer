
from flask import render_template, request, redirect, session, url_for,Flask
from app import app, facebook, twitter, google



@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')


@app.route('/login_fa')
def login_fa():
    return facebook.authorize(callback=url_for('facebook_authorized', next=request.args.get('next') or request.referrer or None, _external=True))


@app.route('/login_fa/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
    # return 'Access denied: reason=%s error=%s' % (
    #     request.args['error_reason'],
    #     request.args['error_description']
    # )
        return redirect(url_for('index'))
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    session['username'] = me.data['name']
    session['user_id'] = me.data['id']
    return redirect(url_for('chat'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/login_tw')
def login_tw():
    return twitter.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))


@app.route('/login_tw/oauth_authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        return redirect(next_url)
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    return redirect(next_url)


@app.route('/google_index')
def google_index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login_go'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login_go'))
        return res.read()

    return res.read()


@app.route('/login_go')
def login_go():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/login_go/authorized')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('google_index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')
