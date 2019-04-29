import docker 
import time
import requests
import re


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
			cli.containers.run("acts",ports={'80/tcp':str(port)},volumes={'database':{'bind':'/app/Database','mode':'rw'}},name="acts"+str(port),remove=True,detach=True)
	time.sleep(1)
