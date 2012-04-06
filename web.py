#!/usr/bin/env python2
import ConfigParser, sqlalchemy, bottle

config = ConfigParser.ConfigParser()
config.read("configs/settings.ini")

db_engine = sqlalchemy.create_engine(config.get("default", "database"))
db_metadata = sqlalchemy.MetaData()

db_monitors = sqlalchemy.Table('monitors', db_metadata,
	sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
	sqlalchemy.Column('host', sqlalchemy.String),
	sqlalchemy.Column('service', sqlalchemy.String),
	sqlalchemy.Column('time', sqlalchemy.TIMESTAMP),
	sqlalchemy.Column('state', sqlalchemy.Integer),
	sqlalchemy.Column('message', sqlalchemy.String)
)

db_metadata.create_all(db_engine)
db_conn = db_engine.connect()

@bottle.route("/")
def index():
	hosts = {}

	# get the latest time
	time = db_conn.execute(db_monitors.select(order_by = sqlalchemy.desc(db_monitors.c.time))).fetchone()[3]

	# get the latest services
	services = db_conn.execute(db_monitors.select(db_monitors.c.time == time))

	# make counters
	counters = {
		"good":		0,
		"warning":	0,
		"bad":		0
	}

	# put the services into the hosts thingy
	for service in services:
		if service[1] not in hosts:
			hosts[service[1]] = []

		# counter
		if service[4] == 1:
			counters["good"] += 1
		elif service[4] == 0:
			counters["bad"] += 1
		elif service[4] == 3:
			counters["warning"] += 1

		hosts[service[1]].append(
			{
				"service":	service[2],
				"state":	service[4],
				"message":	service[5]
			}
		)

	return bottle.template("template.html", hosts = hosts, lastcheck = time, counters = counters)

bottle.debug()
bottle.run()