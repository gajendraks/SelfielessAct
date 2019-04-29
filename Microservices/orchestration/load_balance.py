from flask import Flask, jsonify,render_template,flash,url_for,redirect,request,redirect
import os
import json
import datetime
import time
import requests
import docker
import re

cli = docker.from_env()

app= Flask(__name__)
ptr=-1
count=0

ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]

st_url="http://localhost:"

@app.route("/api/v1/categories",methods = ['GET','POST'])
def list_category():
	if(request.method=='GET'):
		global ptr
		global count
		ptr+=1
		count+=1
		ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
		response=requests.get(st_url+str(ports[ptr%(len(ports))])+"/api/v1/categories")
		cat = response.json()
		return(jsonify(cat),response.status_code)
	if(request.method=='POST'):
		global ptr
		global count
		ptr+=1
		count+=1
		ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
		in_data = request.get_json()
		print(in_data)
		response=requests.post(st_url+str(ports[ptr%(len(ports))])+"/api/v1/categories", json=in_data)
		print(response.status_code)
		return(json.dumps({}),response.status_code)


@app.route("/api/v1/categories/<categoryName>",methods=['DELETE'])
def remove(categoryName):
	global ptr
	global count
	ptr+=1
	count+=1
	ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
	if(request.method=='DELETE'):
		response=requests.delete(st_url+str(ports[ptr%(len(ports))])+"/api/v1/categories/"+categoryName)
		return(jsonify({}),response.status_code)

@app.route("/api/v1/categories/<categoryName>/acts",methods=['GET'])
def list_acts(categoryName):
	global ptr
	global count
	ptr+=1
	count+=1
	ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
	if(request.method=='GET'):
		response=requests.get(st_url+str(ports[ptr%(len(ports))])+"/api/v1/categories/"+categoryName+"/acts")
		ret = response.json()
		return(jsonify(ret),response.status_code)

@app.route("/api/v1/categories/<categoryName>/acts/size",methods=['GET'])
def count_act(categoryName):
	global ptr
	global count
	ptr+=1
	count+=1
	ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
	if(request.method=='GET'):
		response=requests.get(st_url+str(ports[ptr%(len(ports))])+"/api/v1/categories/"+categoryName+"/acts/size")
		ret = response.json()
		return(jsonify(ret),response.status_code)

@app.route("/api/v1/acts/upvote",methods=['POST'])
def upvote():
	global ptr
	global count
	ptr+=1
	count+=1
	ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
	if(request.method=='POST'):
		in_data = request.get_json()
		response=requests.post(st_url+str(ports[ptr%(len(ports))])+"/api/v1/acts/upvote",json=in_data)
		return(jsonify({}),response.status_code)

@app.route("/api/v1/acts/<actId>",methods = ['DELETE'])
def act_delete(actId):
	global ptr
	global count
	ptr+=1
	count+=1
	ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
	if(request.method=='DELETE'):
		response=requests.delete(st_url+str(ports[ptr%(len(ports))])+"/api/v1/acts/"+actId)
		return(jsonify({}),response.status_code)

@app.route("/api/v1/acts",methods=['POST'])
def upload_act():
	global ptr
	global count
	ptr+=1
	count+=1
	ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
	if(request.method=='POST'):
		in_data = request.get_json()
		response=requests.delete(st_url+str(ports[ptr%(len(ports))])+"/api/v1/acts/",json=in_data)
		return(jsonify({}),response.status_code)

@app.route("/api/v1/acts/count",methods = ['GET'])
def total_acts():
	global ptr
	global count
	ptr+=1
	count+=1
	ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
	if(request.method=='GET'):
		response=requests.delete(st_url+str(ports[ptr%(len(ports))])+"/api/v1/acts/count")
		ret = response.json()
		return(jsonify(ret),response.status_code)

@app.route("/api/v1/_count",methods=['GET','DELETE'])
def count1():
	global count
	if(request.method=='GET'):
		return(jsonify([count]),200)
	elif(request.method=='DELETE'):
		count=0
		return('',200)

	return ('',405)



if __name__ == '__main__':
	app.run(host="0.0.0.0",port=80,debug=True)

