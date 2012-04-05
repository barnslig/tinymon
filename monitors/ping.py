import subprocess

class PING:
	def __init__(self, settings):
		self.settings = settings
		self.state = -1

		self.ping()

	def state(self):
		return self.state

	def ping(self):
		ping = subprocess.Popen(
			["ping", "-c", "4", "-i", "0.2", self.settings["host"]],
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE
		)

		out, error = ping.communicate()
		if len(error) == 0:
			out = out.split("\n")
			out = out[len(out)-3]
			out = out.split(" ")

			if "errors," in out:
				self.state = False, "Errors: {0}, Packetloss: {1}, Time: {2}".format(out[5], out[7], out[11])
			else:
				self.state = True, "Time: {0}".format(out[9])
		else:
			self.state = False, error.replace("ping: ", "").replace("\n", "")