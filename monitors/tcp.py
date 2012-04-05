import socket, sys

class TCP:
	def __init__(self, settings):
		self.settings = settings
		self.state = -1

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.connect()

	def state(self):
		return self.state

	def connect(self):
		try:
			self.s.connect((self.settings["host"], self.settings["port"]))
			self.s.shutdown(2)
			self.state = True, ""
		except:
			self.state = False, sys.exc_info()[1]