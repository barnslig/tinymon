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
			lines = out.split("\n")
			res = lines[len(lines)-3]
			res = res.split(" ")

			rtt = lines[len(lines)-2]
			rtt = rtt.split("/")
			rtt = rtt[4]

			if "errors," in out:
				self.state = False, "Errors: {0}, Packetloss: {1}, RTT Avg.: {2} ms".format(res[5], res[7], rtt)
			else:
				self.state = True, "RTT Avg.: {0} ms".format(rtt)
		else:
			self.state = False, error.replace("ping: ", "").replace("\n", "")