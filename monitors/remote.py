import socket, json

class REMOTE:
	def __init__(self, settings):
		self.settings = settings
		self.state = -1
		self.module = settings["module"]

		self.connect()
		self.sendSettings()
		self.dealWithData()

	def state(self):
		return self.state

	def connect(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.settings["remote_host"], self.settings["remote_port"]))

	def sendSettings(self):
		settings = {}

		settings["module"] = self.settings["module"]

		copy_settings = self.settings
		copy_settings.pop("module")
		copy_settings.pop("remote_host")
		copy_settings.pop("remote_port")
		settings["settings"] = copy_settings

		self.s.sendall(json.dumps(settings))

	def dealWithData(self):
		data = self.s.recv(1024)
		data = json.loads(data)
		self.state = data[0], self.module + ":" + data[1]

# print REMOTE({
# 	"remote_port":	65535,
# 	"remote_host":	"127.0.0.1",
# 	"module":		"smtp",
# 	"host":			"caesium.caracl.de",
# 	"port":			25,
# 	"tls":			True
# }).state