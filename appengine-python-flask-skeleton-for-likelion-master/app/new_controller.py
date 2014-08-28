from flask import jsonify,request,render_template
from app import app

@app.route('/')
def test():
	return render_template('test.html')

@app.route('/ajax', methods=['GET','POST'])
def ajax():
	data={}
	data['success']=False
	data['error']="error!!!"

	if request.method=='POST':
		ajax=request.form
		data['result']=int(ajax['ajax1'])+int(ajax['ajax2'])
		data['success']=True
		return jsonify(data)
	else:
		data['error']="not post"
		return jsonify(data)