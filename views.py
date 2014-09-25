# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, session, url_for,Flask,jsonify
from app import app, facebook, twitter, google,db
from sqlalchemy import desc
from app.models import Team,Location_first,University,User
from app.forms import User_register_form,Team_register_form,NonValidatingSelectField, Search_user_name_form, Search_school_name_form, Search_team_name_form
import sys
reload(sys)
sys.setdefaultencoding('UTF8')


@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')





################################################################ teamregister


@app.route('/team_register', methods=['GET','POST'])
def team_register():
    form = Team_register_form()
    teams=Team.query.all()
    location_first=Location_first.query.all()
    if request.method == 'POST':
        if not form.validate():
            return render_template('team_register.html', form=form, teams=teams, location_first=location_first)
        else:
            team=Team(
                teamname=form.teamname.data,
                location=form.location.data.location,
                university=form.university.data,
                Introduce=form.introduce.data,
                favorite_date=form.favorite_date.data,
                favorite_place=form.favorite_place.data,
                ranking_score=0,
                ranking_result="test",
                leader_name="test"
                )


            db.session.add(team)
            db.session.commit()
            return "Nice to meet you"
    else:
        return render_template('team_register.html', form=form, teams=teams, location_first=location_first)

######################################################################################################


@app.route('/user_register', methods=['GET','POST'])
def user_register():
    form = User_register_form()
    teams=Team.query.all()
    location_first=Location_first.query.all()
    if request.method == 'POST':
        if not form.validate():
            return render_template('user_register.html', form=form, teams=teams, location_first=location_first)
        else:
            user=User(
                team_id=1,
                email="test",
                name=form.user_name.data,
                phone_number=form.phone_number.data,
                university=form.university.data
                )

            db.session.add(user)
            db.session.commit()

        
            return "success!!"
    else:
        return render_template('user_register.html', form=form, teams=teams, location_first=location_first)

#########################################################################################


@app.route('/location_university', methods=["GET", "POST"])
def location_university():
    data={}
    university_list=[]
    university={}
    data["success"]=False
    if request.method =='POST':
        location_id=request.form.get('location_id')
        university_instance_dictionary=db.session.query(University).filter(University.location_id == location_id).all()
        for university_instance in university_instance_dictionary:
            university['id']=university_instance.id
            university['university']=university_instance.university
            university['location_id']=university_instance.location_id
            university['address']=university_instance.address
            university_list.append(university)
            university={}
        data["university"]=university_list
        return jsonify(data)



@app.route('/add/test', methods=["GET", "POST"])
def add_test():
    data = {}
    data["success"] = False
    if request.method == "POST":
        req = request.form
        data["result"] = int(req["number1"]) + int(req["number2"])
        data["success"] = True
        return jsonify(data)
    data["error"] = "Not GET methods, POST methods plz"
    return jsonify(data)










###################################################################################login




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
     return redirect(url_for('index'))
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


##################################################################################


@app.route('/team_search_location', methods=["GET", "POST"])
def team_search_location():
    if request.method == 'GET':
        return render_template('team_search_location.html')
    else:
        location_id = request.form.get('location_id') 
        school_list = db.session.query(University).filter(University.location_id==location_id).all() 
        resp = {}
        resp["data"] = []
        temp = {}
        for school in school_list:
            temp['id'] = school.id
            temp['university'] = school.university
            temp['location_id'] = school.location_id
            temp['address'] = school.address
            resp['data'].append(temp)
            temp = {}
        return jsonify(resp)
######################################################################################### Search by user, schoolname, teamname

@app.route('/search_name_user', methods=["GET", "POST"])
def search_name_user():
    form = Search_user_name_form()
    if request.method == 'GET':
        return render_template('search_name_user.html', form=form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('search_name_user.html', form=form)
        else:
            result_list = db.session.query(User).filter(User.name.contains(form.username.data)).all()
            return render_template('search_name_user.html', form=form, result_list=result_list)
    return render_template('search_name_user.html', form=form)


@app.route('/search_name_school', methods=["GET", "POST"])
def search_name_school():
    form = Search_school_name_form()
    if request.method == 'GET':
        return render_template('search_name_school.html', form=form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('search_name_school.html', form=form)
        else:
            result_list = db.session.query(University).filter(University.university.contains(form.schoolname.data)).all()
            return render_template('search_name_school.html', form=form, result_list=result_list)
    return render_template('search_name_school.html', form=form)


@app.route('/seach_name_team', methods=["GET", "POST"])
def search_name_team():
    form = Search_team_name_form()
    if request.method == 'GET':
        return render_template('search_name_team.html', form=form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('search_name_team.html', form=form)
        else:
            result_list = db.session.query(Team).filter(Team.teamname.contains(form.teamname.data)).all()
            return render_template('search_name_team.html', form=form, result_list=result_list)
    return render_template('search_name_team.html', form=form)

#########################################################################################################


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')