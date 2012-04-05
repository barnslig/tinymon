import smtplib, sys, time

class SMTP:
	def __init__(self, settings):
		self.settings = settings
		self.state = -1
		try:
			self.smtp = smtplib.SMTP(self.settings["host"], self.settings["port"], timeout=3)
			self.ehlo = self.smtp.ehlo()
			self.state = True, ""

			self.startTLS()
			if type(self.state).__name__ == "bool":
				self.login()

		except:
			self.state = False, "Problem while connecting: {0}".format(sys.exc_info()[1])

		time.sleep(1)

	def state(self):
		return self.state

	def startTLS(self):
		if self.settings["tls"] == True:
			try:
				self.smtp.starttls()
				self.state = True, "StartTLS successfull."
			except:
				self.state = False, "Problem with StartTLS: {0}".format(sys.exc_info()[1])

	def login(self):
		if "username" in self.settings:
			if "password" in self.settings:
				if "AUTH PLAIN" in self.ehlo[1]:
					try:
						self.smtp.login(self.settings["username"], self.settings["password"])
						self.state = True, "Login successfull."
					except:
						self.state = False, "Problem with the authentication: {0}".format(sys.exc_info()[1])
				else:
					self.state = 3, "No Authentication supported."