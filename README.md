# selfilessact
cloud computing project


Implemented a custom container orchestrator engine that will:

There are three parts in orchestration:
◦ server.py (for load-balancing)
▪ redirects request to containers in round robin fashion
▪ Load balance all incoming HTTP requests (to the Acts EC2
instance) equally between all running Acts containers in a
round-robin fashion.
◦ autoscaling.py(for autoscale)
▪ It starts container with port 8000 with name acts8000
▪ Checks no_of request every 2min and scales respectively.
▪ Increase the number of Acts containers if the network
load increases above a certain threshold.
◦ fault_tolerance.py(for fault_tolerance)
▪ If any thing crashes then starts automatically.
▪ Monitor the health of each container through a health
check API every 1min, and if a container is found to be
unhealthy, stop the container and start a new one to
replace it.

New container gets created with parameters
name = acts+port_no
volume attached = database
detached mode
remove=True gets removed from storage when process gets
killed environment = [user_ip] environment variable for user ip as it
is not elastic
➢ How to run
➢ Build docker in both containers
➢ run make command for (server,scale,fault) in three different
terminals
