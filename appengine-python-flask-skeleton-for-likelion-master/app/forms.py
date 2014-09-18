# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (
	StringField,
	PasswordField,
	TextAreaField,
	SubmitField,
	SelectField
)
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Team,Location_first,University
# from wtforms import Form
# from wtforms_components import PhoneNumberField


def location_first():
	return Location_first.query.filter(Location_first.upper_id==0)






class User_register_form(Form):

	user_name = StringField(
		u'이름',
		[validators.data_required(u'이름을 입력하시기 바랍니다.')],
		description={'placeholder': u'이름을 입력하세요.'}
	)
	# phone_number = PhoneNumberField(
	# 	country_code='FI',
	# 	display_format='national' 
	# 	)
	
	phone_number = StringField(
		u'핸드폰',
		[validators.data_required(u'폰번을 입력하시기 바랍니다.')],
		description={'placeholder': u'폰번을 입력하세요.'}
	)

	location_first = QuerySelectField('location_first',query_factory=location_first,get_label='location',allow_blank=True)


	university = StringField(
		u'대학교',
		[validators.data_required(u'대학명을 입력하시기 바랍니다.')],
		description={'placeholder': u'대학명을 입력하세요.'}
	)

	submit = SubmitField("다음단계")

class NonValidatingSelectField(SelectField):
	def pre_validate(self, form):
		pass



class Team_register_form(Form):

	teamname = StringField(
		u'팀이름',
		[validators.data_required(u'이름을 입력하시기 바랍니다.')],
		description={'placeholder': u'이름을 입력하세요.'}
	)
	
	location = QuerySelectField('location_first',query_factory=location_first,get_label='location',allow_blank=True)

	university= NonValidatingSelectField(u'대학교', choices=[])


	introduce= TextAreaField(
		u'팀소개',
		[validators.data_required(u'팀소개를 입력하시기 바랍니다.')],
		description={'placeholder': u'팀소개를 입력하세요.'}
		)
	
	favorite_date = SelectField(u'선호요일', choices=[('월요일', '월요일'),('화요일','화요일'),('수요일','수요일'),('목요일','목요일'),('금요일','금요일'),('토요일','토요일'),('일요일','일요일')])

	favorite_place = StringField(
		u'선호장소',
		[validators.data_required(u'대학명을 입력하시기 바랍니다.')],
		description={'placeholder': u'대학명을 입력하세요.'}
	)

	submit = SubmitField("다음단계")