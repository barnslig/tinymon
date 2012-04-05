#!/usr/bin/env python2
import ConfigParser, signal, sqlalchemy, datetime

settings = {
	"config":	"configs/settings.ini",
	"hosts":	"configs/hosts.ini"
}

config = ConfigParser.ConfigParser()
config.read(settings["config"])

hosts = ConfigParser.ConfigParser()
hosts.read(settings["hosts"])

db_engine = sqlalchemy.create_engine(config.get("default", "database"))
db_metadata = sqlalchemy.MetaData()

db_monitors = sqlalchemy.Table('monitors', db_metadata,
	sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
	sqlalchemy.Column('host', sqlalchemy.String),
	sqlalchemy.Column('service', sqlalchemy.String),
	sqlalchemy.Column('time', sqlalchemy.TIMESTAMP),
	sqlalchemy.Column('state', sqlalchemy.Boolean),
	sqlalchemy.Column('message', sqlalchemy.String)
)

db_metadata.create_all(db_engine)
db_conn = db_engine.connect()

modules = []

time = datetime.datetime.now()

# make the tests
for host in hosts.sections():
	this = host.split(":")

	if this[1] not in modules:
		exec("import monitors.{0}".format(this[1]))
		modules.append(this[1])

	# settings
	settings = {
		"host": this[0]
	}
	for option in hosts.options(host):
		if hosts.get(host, option) == "on":
			settings[option] = True
		elif hosts.get(host, option) == "off":
			settings[option] = False
		else:
			try:
				settings[option] = int(hosts.get(host, option))
			except:
				settings[option] = hosts.get(host, option)

	# test
	exec("test = monitors.{0}.{1}(settings).state".format(this[1], this[1].upper()))

	# the sql foobar
	test_sql = db_monitors.insert().values(
		host = this[0],
		service = this[1],
		time = time,
		state = test[0],
		message = test[1]
	)
	db_conn.execute(test_sql)