#mysite/start_redis_server.py
import os

try:
	import docker
	client = docker.from_env()
	running_container_images = [str(i.image) for i in client.containers.list()]	
	if "<Image: 'redis:2.8'>" in running_container_images:
		print ("Redis server already running")
	else:
		print ("starting redis server by docker run -p 6379:6379 -d redis:2.8")
		os.system("docker run -p 6379:6379 -d redis:2.8")

	
except ImportError as error:
	print (error, 'found','\n Please install by "pip3 install docker"')