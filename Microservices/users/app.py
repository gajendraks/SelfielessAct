from flask import Flask, jsonify,render_template,flash,url_for,redirect,request
import os
import json
import time
# from werkzeug.local import LocalProxy
import csv
import re
import datetime
import time
from flask_cors import CORS

def is_sha1(maybe_sha):
    if len(maybe_sha) != 40:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True




app= Flask(__name__)
CORS(app)


@app.route("/multi/<int:num>",methods=['GET'])
def hello(num):
	return jsonify({"about":"hello_world gajendra","result":num*10})

# Add user
@app.route("/api/v1/users",methods=['POST','GET'])
def users_verify():
	if(request.method=='POST'):
		data = request.get_json()
		# print(type(data))

		#if request is other than dictionary/json format
		if(type(data)!= dict):
			return('request error',400)
		#if username and password does not exist in request
		if(("username" not in data.keys()) or ("password" not in data.keys())):
			return ('not there',400)
		
		usname = data["username"]
		pword = data['password']

		#checking password format is there in sha1 
		if(not is_sha1(pword)):
			return ('password',400)
		
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

	if(request.method=='GET'):
		if(not(os.path.exists("Database/users.txt"))):
			return('',204)
			# file_1.seek(0)
		else:
			file_1 = open("Database/users.txt",'r')

		d={}
		d=json.load(file_1)
		file_1.close()
		l=list(d.keys())
		return (jsonify(l),200)		

	return ('',405)

	
# Remove user
@app.route("/api/v1/users/<username>",methods = ['DELETE'])
def delete(username):
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






if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0")
