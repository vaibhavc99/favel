from python_on_whales import DockerClient

class Containers:
	def __init__(self):
		self.docker = DockerClient(compose_files=["./ContainerService/docker-compose.yml"])

	def start_containers(self):
		self.docker.compose.up(detach=True)

	def stop_containers(self):
		self.docker.compose.stop()

	def remove_containers(self):
		self.docker.compose.down()

	def staus(self):
		for container in self.docker.compose.ps():
			print(container.name, container.state.status)

