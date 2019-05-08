import docker 
import time
import requests
import re

ip = "13.127.91.65"
user_ip = "user_ip="+ip

cli = docker.from_env()


containers={}


ip = "localhost"
while(1):
	# print("hello")
	list_cont = [y for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
	for conta in list_cont:
		print("hello",conta)
		port = conta.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
		url = "http://"+ip+":"+port+"/api/v1/_health"
		res = requests.get(url)
		if(res.status_code==500):
			print("hello")
			conta.kill()
			ports = [int(y.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']) for y in cli.containers.list() if re.match(r"/acts800[0-9]",y.attrs['Name'])]
			print(ports)
			cli.containers.run("acts",ports={'80/tcp':str(port)},volumes={'database':{'bind':'/app/Database','mode':'rw'}},name="acts"+str(port),environment = [user_ip],remove=True,detach=True)
			print("over")
	time.sleep(1)