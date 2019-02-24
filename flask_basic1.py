from flask import Flask, jsonify,render_template,flash,url_for,redirect,request
from werkzeug import secure_filename
import os
import json
import time
from werkzeug.local import LocalProxy
import csv
import re
import datetime
import time

def isTimeFormat(input):
    try:
	    datetime.datetime.strptime(input[:input.find(":")], '%d-%m-%Y')
	    time.strptime(input[input.find(":")+1:], '%H-%M-%S')
	    return True
    except ValueError:
	    return False


act_id=0
acts={}


app= Flask(__name__)
print(app)
@app.route("/multi/<int:num>",methods=['GET'])
def hello(num):
	return jsonify({"about":"hello_world gajendra","result":num*10})

# Add user
@app.route("/api/v1/users",methods=['POST'])
def users_verify():
	if(request.method=='POST'):
		data = request.get_json(force=True)
		print(len(request.get_json().keys()))
		usname = data["username"]
		pword = data['password']
		
		if(not(os.path.exists("Database/users.txt"))):
			file_1 = open("Database/users.txt",'w')
			file_1.write("{}")
			# file_1.seek(0)
			file_1.close()
			file_1 = open("Database/users.txt",'r+')
		else:
			file_1 = open("Database/users.txt",'r+')
		
		d={}
		d=json.load(file_1)
		file_1.close()
		if(usname in d.keys()):
			return ('',400)
		# d.seek()
		d[usname]=pword
		file_1 = open("Database/users.txt",'w')
		json.dump(d,file_1)
		file_1.close()
		return ('',201)
	return ('',405)

	
# Remove user
@app.route("/api/v1/users/<username>",methods = ['DELETE'])
def delete(username):
	print(request.method)
	# print(request.get_json()['caption'])
	if(request.method=='DELETE'):
		uname = username
		if(not(os.path.exists("Database/users.txt"))):
			return('',400)
		file_1 = open("Database/users.txt",'r+')
		d={}
		d=json.load(file_1)
		if(not(uname in d.keys())):
			return ('',400)
		d.pop(uname)
		file_1.close()
		file_1 = open("Database/users.txt",'w')
		json.dump(d,file_1)
		file_1.close()
		return ('',200)
	return ('',405)

# list all categories, add a category , remove a category
@app.route("/api/v1/categories",methods = ['GET','POST'])
def list():
	print("Hello")
	if(request.method=='GET'):
		if(not(os.path.exists("Database/categories.txt"))):
			f = open("Database/categories.txt",'w')
			f.write('{}')
			f.close()
			f = open("Database/categories.txt",'r+')
		else:
			f = open("Database/categories.txt",'r+')
		d={}
		d=json.load(f)
		f.close()
		for key in d.keys():
			d[key] = len(d[key])
		return jsonify(d),200
	
	if(request.method=='POST'):
		if('categoryName' not in request.get_json().keys()):
			return ('',400)
		category_name = request.get_json()['categoryName']
		if(not(os.path.exists("Database/categories.txt"))):
			print('hello')
			f = open("Database/categories.txt",'w')
			f.write('{}')
			f.close()
			f = open("Database/categories.txt",'r+')
		else:
			f = open("Database/categories.txt",'r+')
		d={}
		d=json.load(f)
		f.close()
		if(category_name in d.keys()):
			return('',400)
		d[category_name]=[]
		f = open("Database/categories.txt",'w')
		json.dump(d,f)
		f.close()

		return ('',201)

	return ('',405)

""" # add category
@app.route("/api/category/add",methods=['POST'])
def add():
	if(request.method=='POST'):
		category_name = request.get_json()['categoryName']
		if(not(os.path.exists("Database/categories.txt"))):
			print('hello')
			f = open("Database/categories.txt",'w')
			f.write('{}')
			f.close()
			f = open("Database/categories.txt",'r+')
		else:
			f = open("Database/categories.txt",'r+')
		d={}
		d=json.load(f)
		f.close()
		if(category_name in d.keys()):
			return('',400)
		d[category_name]=[]
		f = open("Database/categories.txt",'w')
		json.dump(d,f)
		f.close()

		return ('',201)
		
		# if(os.path.exists("static/"+category_name)):
		# 	# print("exists")
		# 	return('',400)
		# else:
		# 	os.mkdir("static/"+category_name)
		# 	return ('',200)

	return ('',405) """
	
@app.route("/api/v1/categories/<categoryName>",methods=['DELETE'])
def remove(categoryName):
	if(request.method=='DELETE'):
		if(not(os.path.exists("Database/categories.txt"))):
			return('',400)
		else:
			f = open("Database/categories.txt",'r+')
		d={}
		d=json.load(f)
		f.close()
		if(categoryName not in d.keys()):
			return('',400)
		d[categoryName]=[]
		d.pop(categoryName)

		f = open("Database/categories.txt",'w')
		json.dump(d,f)
		f.close()
		return('',200)

		
	return ('',405)



# list acts for a give categoryname
@app.route("/api/v1/categories/<categoryName>/acts",methods=['GET'])
def list_acts(categoryName):
	# print(categoryName)
	if(request.method=='GET'):
		if(not(os.path.exists("Database/categories.txt"	))):
			print("doesnot exist")
			return('Categories does not exist ',204)
		category_f = open("Database/categories.txt",'r+')
		cat_d={}
		cat_d=json.load(category_f)
		category_f.close()
		if(categoryName not in cat_d.keys()):
			return ('category doesnot exist',204)
		acts_list = cat_d[categoryName]
		if(request.args.get('start')!=None):
			st=request.args.get('start')
			en=request.args.get('end')
			st=int(st)
			en=int(en)
			out_list=[x for x in acts_list if st<=int(x)<=en]
			


			
			length = len(out_list)
			return(jsonify(length),200) 
		else:
			if(len(acts_list)>100):
				return('',413)
			acts_f = open("Database/acts.txt",'r+')
			acts_d = {}
			acts_d = json.load(acts_f)
			acts_f.close()
			upvote_f = open("Database/upvote.txt",'r+')
			upvote_d = {}
			upvote_d = json.load(upvote_f)
			upvote_f.close()
			output = {}
			for actid in acts_list:
				output[actid] = acts_d[actid]
				output[actid]["upvotes"] = upvote_d[actid]
			return (jsonify(output),200)
	else:
		return('',405)

# List number of acts for a given category
@app.route("/api/v1/categories/<categoryName>/acts/size",methods=['GET'])
def count_act(categoryName):
	print(categoryName)
	if(request.method=='GET'):
		if(not(os.path.exists("Database/categories.txt"	))):
			print("doesnot exist")
			return('Categories does not exist ',204)
		category_f = open("Database/categories.txt",'r+')
		cat_d={}
		cat_d=json.load(category_f)
		category_f.close()
		if(categoryName not in cat_d.keys()):
			return ('category doesnot exist',204)
		acts_list = cat_d[categoryName]
		length = len(acts_list)
		return(jsonify(length),200)
		
	else:
		return('',405)

# Upvote an act
@app.route("/api/v1/acts/upvote",methods=['POST'])
def upvote():
	if(request.method=='POST'):
		actid=request.get_json()['actID']
		if(not(os.path.exists("Database/upvote.txt"))):
			upvote_f = open("Database/upvote.txt",'w')
			upvote_f.write("{}")
			# f.seek(0)
			upvote_f.close()
			upvote_f = open("Database/upvote.txt",'r+')
		else:
			upvote_f = open("Database/upvote.txt",'r+')
		d={}
		d=json.load(upvote_f)
		upvote_f.close()
		if(actid not in d.keys()):
			return('',400)
		d[actid]=d[actid]+1
		upvote_f = open("Database/upvote.txt",'w')
		json.dump(d,upvote_f)
		return ('',200)
	return ('',405)

# Remove an act
@app.route("/api/v1/acts/<actId>",methods = ['DELETE'])
def act_delete(actId):
	if(request.method=='DELETE'):
		if(not(os.path.exists("Database/acts.txt"))):
			return('',400)
		act_f = open("Database/acts.txt",'r+')
		d={}
		d=json.load(act_f)
		if(actId not in d.keys()):
			return ('',400)
		category_name = d[actId]["categoryName"]	
		d.pop(actId)
		act_f.close()
		act_f = open("Database/acts.txt",'w')
		json.dump(d,act_f)
		act_f.close()


		cat_f = open("Database/categories.txt",'r+')
		d={}
		d=json.load(cat_f)
		d[category_name].remove(actId)
		cat_f.close()
		cat_f = open("Database/categories.txt",'w')
		json.dump(d,cat_f)
		cat_f.close()

		upvote_f = open("Database/upvote.txt",'r+')
		d={}
		d=json.load(upvote_f)
		d.pop(actId)
		upvote_f.close()
		upvote_f = open("Database/upvote.txt",'w')
		json.dump(d,upvote_f)
		upvote_f.close()

		return ('',200)
	return ('',405)
			

# uplupload an act
@app.route("/api/v1/acts",methods=['POST'])
def upload_act():
	if(request.method=='POST'):
		
		# taking input from form data

		actId = request.get_json()['actId']
		username = request.get_json()['username']
		timestamp = request.get_json()['timestamp']
		caption = request.get_json()['caption']
		categoryName = request.get_json()['categoryName']
		imgB64 = request.get_json()['imgB64']
		input_keys = request.get_json().keys()
		
		
		# if upvotes are present then send apprpriate code

		if("upvotes" in input_keys):
			return ('upvotes',400)

		# if acts.txt doesn't exist then create

		if(not(os.path.exists("Database/acts.txt"))):
			acts_f = open("Database/acts.txt",'w')
			acts_f.write("{}")
			# f.seek(0)
			acts_f.close()
			acts_f = open("Database/acts.txt",'r+')
		else:
			acts_f = open("Database/acts.txt",'r+')
		
		# define dictionary to load from file
		
		d={}
		d=json.load(acts_f)
		acts_f.close()

		# checking actid exist or not
		
		if(actId not in d.keys()):
			#format checking for timestamp
			if(not isTimeFormat(timestamp)):
				return('time',400)


			#checking if user exists and opening user file

			user_f = open("Database/users.txt",'r+')
			user_d = {}
			user_d=json.load(user_f)
			if(username not in user_d.keys()):
				return('uname',400)
			user_f.close()


			#checking if image string matches with base64

			""" if(not(re.match("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$",imgB64))):
				return('img',400) """
			
			
			#checking for category name and opening category file
			if(not(os.path.exists("Database/categories.txt"))):
				return ('',400)
			cat_f = open("Database/categories.txt",'r+')
			cat_d = {}
			cat_d=json.load(cat_f)
			cat_f.close()
			if(categoryName not in cat_d.keys()):
				return ('category',400)
			cat_d[categoryName].append(actId)
			cat_f = open("Database/categories.txt",'w')
			json.dump(cat_d,cat_f)
			cat_f.close()

			if(not(os.path.exists("Database/upvote.txt"))):
				upvote_f = open("Database/upvote.txt",'w')
				upvote_f.write("{}")
				# f.seek(0)
				upvote_f.close()
				upvote_f = open("Database/upvote.txt",'r+')
			else:
				upvote_f = open("Database/upvote.txt",'r+')

			#now create list for act id 
			dict_value = {"username":username,"timestamp":timestamp,"caption":caption,"categoryName":categoryName,"imgB64":imgB64}
			# l=[username,timestamp,caption,categoryName,imgB64]
			d[actId]=dict_value
			upvote_d = {}
			upvote_d = json.load(upvote_f)
			upvote_f.close()
			upvote_d[actId]=0
			upvote_f = open("Database/upvote.txt",'w')
			json.dump(upvote_d,upvote_f)
			f = open("Database/acts.txt",'w')
			json.dump(d,f)
			f.close()
			return ('',201)
		else:
			return ('actid',400)

	return ('',405)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404




if __name__ == '__main__':
	app.run(debug=True)