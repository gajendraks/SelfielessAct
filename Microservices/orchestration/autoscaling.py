import re
import docker 
import time
import requests
import json

ip = "13.127.91.65"
user_ip = "user_ip="+ip

cli = docker.from_env()
# cont_list = cli.containers.list()
# no_containers = len(cont_list)
port = 8000
cli.containers.run("acts",ports={'80/tcp':str(port)},volumes={'database':{'bind':'/app/Database','mode':'rw'}},name="acts"+str(port),environment = [user_ip],remove=True,detach=True)

while(1):
	# time.sleep(120)
	count = requests.get("http://localhost/api/v1/_count")
	count = count.json()[0]
	requests.delete("http://localhost/api/v1/_count")
	cont_list = cli.containers.list()
	no_containers = len(cont_list)
	if(count<20):
		for i in [y for y in cli.containers.list() if re.match(r"/acts800[^0]",y.attrs['Name'])]:
			i.kill()
			port-=1
	elif(count<40):
		for i in [y for y in cli.containers.list() if re.match(r"/acts800[^01]",y.attrs['Name'])]:
			i.kill()
			port-=1
		print(port)
		l=[y for y in cli.containers.list() if re.match(r"/acts800",y.attrs['Name'])]
		for i in range(len(l),2):
			port+=1
			cli.containers.run("acts",ports={'80/tcp':str(port)},volumes={'database':{'bind':'/app/Database','mode':'rw'}},name="acts"+str(port),environment = [user_ip],remove=True,detach=True)
	elif(count>60):
		for i in [y for y in cli.containers.list() if re.match(r"/acts800[^012]",y.attrs['Name'])]:
			i.kill()
			port-=1
		l=[y for y in cli.containers.list() if re.match(r"/acts800",y.attrs['Name'])]
		for i in range(len(l),3):
			port+=1
			cli.containers.run("acts",ports={'80/tcp':str(port)},volumes={'database':{'bind':'/app/Database','mode':'rw'}},name="acts"+str(port),environment = [user_ip],remove=True,detach=True)
	elif(count>=60):
		for i in [y for y in cli.containers.list() if re.match(r"/acts800[^0123]",y.attrs['Name'])]:
			i.kill()
			port-=1
		l=[y for y in cli.containers.list() if re.match(r"/acts800",y.attrs['Name'])]
		for i in range(len(l),4):
			port+=1
			cli.containers.run("acts",ports={'80/tcp':str(port)},volumes={'database':{'bind':'/app/Database','mode':'rw'}},name="acts"+str(port),environment = [user_ip],remove=True,detach=True)

	time.sleep(120)