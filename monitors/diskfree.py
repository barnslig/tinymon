import subprocess

class DISKFREE:
	def __init__(self, settings):
		self.settings = settings
		self.state = -1
		self.overlimit = []

		self.getDiskFree()

	def state(self):
		return self.state

	def buildState(self):
		output = ""
		for disk in self.overlimit:
			output += "{0} reached {1}%, {2} left. ".format(disk[2], str(disk[1]), disk[3])
			
			if self.state != False:
				self.state = disk[0]

		self.state = self.state, output

	def getDiskFree(self):
		df = subprocess.Popen(
			"df -h",
			shell = True,
			stdout = subprocess.PIPE
		)
		out = df.communicate()

		for disk in out[0].split("\n"):
			if disk[0:10] != "Filesystem":
				if len(disk) > 0:
					line = disk.split(" ")
					filling = int(line[len(line)-2].replace("%", ""))
					if filling >= 90:
						self.overlimit.append((False, filling, line[len(line)-1], line[len(line)-4]))
					elif filling >= 75:
						self.overlimit.append((3, filling, line[len(line)-1], line[len(line)-4]))

		self.buildState()