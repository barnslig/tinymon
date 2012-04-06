import urllib2, sys

class HTTP:
	def __init__(self, settings):
		self.settings = settings
		self.state = -1
		self.url = ""

		self.buildURL()

		self.http()

	def state(self):
		return self.state

	def buildURL(self):
		self.url = "http://" + self.settings["host"]
		if "port" in self.settings:
			self.url = self.url + ":" + str(self.settings["port"])

	def http(self):
		try:
			http = urllib2.urlopen(self.url, timeout=3)
			if http.code == 200:
				self.state = True, "HTTP Status: {0} {1}".format(str(http.code), http.msg)
			else:
				self.state = 3, "HTTP Status: {0} {1}".format(str(http.code), http.msg)
		except urllib2.HTTPError, e:
			self.state = False, "HTTP Status: {0} {1}".format(str(e.code), e.msg)
		except:
			self.state = False, sys.exc_info()[1]