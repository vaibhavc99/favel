from python_on_whales import docker

class Containers:

	def start_containers(self):
		docker.compose.up(detach=True)

	def stop_containers(self):
		docker.compose.stop()

	def remove_containers(self):
		docker.compose.down()

	def staus(self):
		for container in docker.compose.ps():
			print(container.name, container.state.status)

#Just to test

c = Containers()		
c.start_containers()
c.staus()
c.stop_containers()
