import imaplib, sys, signal

class IMAP:
	def __init__(self, settings):
		self.settings = settings
		self.state = -1
		self.timeoutEnabled = False

		signal.signal(signal.SIGALRM, self.timeout)
		signal.alarm(3)

		self.connect()

		if self.state[0] == True:
			self.login()

		if self.state[0] == True:
			self.imap.close()
			self.imap.logout()

		if self.timeoutEnabled == True:
			self.state = False, "Login timed out"

	def state(self):
		return self.state

	def connect(self):
		try:
			if self.settings["ssl"] == True:
				self.imap = imaplib.IMAP4_SSL(self.settings["host"], self.settings["port"])
			else:
				self.imap = imaplib.IMAP4(self.settings["host"], self.settings["port"])

			self.state = True, ""
		except:
			self.state = False, "Error while connecting: {0}".format(sys.exc_info()[1])

	def timeout(self, foo, bar):
		self.timeoutEnabled = True

		# dirty hack: raise any exception
		self.imap.bar()

	def login(self):
		try:
			self.imap.login(self.settings["username"], self.settings["password"])
			self.imap.select()
			self.state = True, ""
		except:
			self.state = False, "Error while authentication: {0}".format(sys.exc_info()[1])