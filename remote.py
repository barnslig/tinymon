#!/usr/bin/env python2
import socket, json

host = ""
port = 65535

modules = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

while True:
	conn, addr = s.accept()

	while True:
		data = conn.recv(1024)
		if not data:
			break

		try:
			data = json.loads(data)

			if data["module"] not in modules:
				exec("import monitors.{0}".format(data["module"]))
				modules.append(data["module"])

			exec("test = monitors.{0}.{1}(data['settings']).state".format(data["module"], data["module"].upper()))

			conn.sendall(json.dumps(test))
		except:
			pass

conn.close()
s.close()