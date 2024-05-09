import psycopg2
import dbSecret

class Database:
	def __init__(self):
		self.lock = False
		self.conn = self.connect()
		self.cur = self.conn.cursor()

	def __del__(self):
		if hasattr(self, "cur"):
			self.cur.close()
		if hasattr(self, "conn"):
			self.conn.close()

	def connect(self):
		conn = psycopg2.connect(
			user = dbSecret.dbusername, 
			password = dbSecret.dbpassword,
			host = dbSecret.dbhost,
			port = dbSecret.dbport,
			dbname = dbSecret.dbname 
		)
		return conn

	def createTables(self):
        # Type 0 = normal user, 1 = "employee", 2 = admin
		# self.cur.execute("""DROP TABLE users""")
		self.cur.execute("""DROP TABLE jobApplications""")
		self.cur.execute("""DROP TABLE jobAdvertisements""")

		# self.cur.execute("""
		# 	CREATE TABLE users (
		# 		id serial PRIMARY KEY,
		# 		username TEXT NOT NULL,
		# 		hashedPsw TEXT NOT NULL,
		# 		type INT
		# 	)
		#  """)

				# userId INTEGER REFERENCES users(id),
		
		self.cur.execute("""
			CREATE TABLE jobAdvertisements (
				id serial PRIMARY KEY,
				url TEXT NOT NULL,
				title TEXT NOT NULL,
				description TEXT NOT NULL,
				location TEXT NOT NULL
			)
		""")

        # Status 0 = pending rewiev, 1 = to next step, 2 = disqualified
		self.cur.execute("""
			CREATE TABLE jobApplications (
				id serial PRIMARY KEY,
				position INTEGER REFERENCES jobAdvertisements(id),
				name TEXT NOT NULL,
				email TEXT NOT NULL,
				coverLetter TEXT NOT NULL,
                status INT DEFAULT 0
			)
		""")

		self.conn.commit()

	def getAdvertisements(self):
		self.cur.execute( "SELECT * FROM jobAdvertisements" )
		return self.cur.fetchall()

	def getAdvertisement(self, adId):
		self.cur.execute( "SELECT * FROM jobAdvertisements WHERE id = %s" ,(adId,))
		return self.cur.fetchall()

	def createAdvertisements(self, url ,title, description, location):
		self.cur.execute( 
			"INSERT INTO jobAdvertisements (url ,title, description, location) VALUES (%s,%s,%s,%s)",
			(url ,title, description, location) 
		)
		return self.conn.commit()

	def addApplication(self, position, name, email, coverLetter, status):
		self.cur.execute( 
			"INSERT INTO jobApplications (position, name, email, coverLetter) VALUES (%s,%s,%s,%s)",
			(position, name, email, coverLetter) 
		)
		return self.conn.commit()

	def getAdvertisementLinks(self):
		self.cur.execute( "SELECT id FROM jobAdvertisements" )
		return self.cur.fetchall()

	def linkAddToName(self):
		self.cur.execute( "SELECT id, title FROM jobAdvertisements" )
		return self.cur.fetchall()

	def getApplications(self):
		self.cur.execute( "SELECT position, name, email, coverLetter, id, status FROM jobApplications" )
		applications = self.cur.fetchall()
		return [{"position":appli[0], "name":appli[1], "email":appli[2], "cl":appli[3], "id":appli[4], "status":appli[5]} for appli in applications]

	def getApplicationsWithStatus(self, status):
		self.cur.execute( "SELECT position, name, email, coverLetter, id, status FROM jobApplications WHERE status = %s" ,(status,))
		applications = self.cur.fetchall()
		return [{"position":appli[0], "name":appli[1], "email":appli[2], "cl":appli[3], "id":appli[4], "status":appli[5]} for appli in applications]

	def getApplicationIds(self, status):
		self.cur.execute( "SELECT id FROM jobApplications WHERE status = %s" ,(status,))
		applications = self.cur.fetchall()
		if len(applications) == 0:
			return []
		# return {appli for appli in applications}
		return [appli[0] for appli in applications]

	def disqualifyApplication(self, id):
		self.cur.execute( 
			"UPDATE jobApplications SET status = %s WHERE id = %s",
			(2, id) 
		)
		return self.conn.commit()

	def qualifyApplication(self, id):
		self.cur.execute( 
			"UPDATE jobApplications SET status = %s WHERE id = %s",
			(1, id) 
		)
		return self.conn.commit()

	def getStatusIds(self):
		return [0,1,2]

	def statusIdToStr(self, id):
		if id == 0:
			return "Pending review"
		if id == 1:
			return "Waiting for an interview"
		if id == 2:
			return "Rejeted"
		return None

db = Database()
