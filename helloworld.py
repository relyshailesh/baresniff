import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
		<html>
		   <body>
		      <form action="/baresniff/activities" method="post">
		         <div><textarea name="action" rows="3" cols="60"></textarea></div>
			 <div><textarea name="location" rows ="1" cols="30"></textarea></div>
			 <div><textarea name="date" rows = "1" cols="30"></textarea></div>
			 <div><input type="submit" value="Sign Guestbook"></div>
		      </form>
		   </body>
	        </html>""")

class RootHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>You wrote:<pre>')
		self.response.out.write('</pre></body></html>')

class Place(db.Model):
	location = db.StringProperty(multiline=True)

class User(db.Model):
	name = db.StringProperty()
	sex = db.BooleanProperty()

class AuditTrail(db.Model):
	createdBy = User()
	modifiedBy = User()
	createdAt = db.DateTimeProperty(auto_now_add=True)
	modifiedAt = db.DateTimeProperty(auto_now_add=True)

class Activity(db.Model):
	action = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	place = Place()
	auditTrail = AuditTrail()

def baresniff_key(baresniff_name=None):
	"""creating db key """
	return db.Key.from_path('Baresniff', baresniff_name or 'thisisit')

class ActivitiesHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')

		# Get all the activities
		activities = db.GqlQuery("SELECT * "
				"FROM Activity "
				"WHERE ANCESTOR IS :1 "
				"ORDER BY date DESC LIMIT 10",
				baresniff_key())
		self.response.out.write(activities)
		self.response.out.write('</body></html>')

	def post(self):
		self.response.out.write('<html><body> posting the activity')

		#post the activity
		activity = Activity()
		activity.action = self.request.get('action')
		activity.put()



	def put(self):
		self.response.out.write('<html><body> updating the activity')



	def delete(self):
		self.response.out.write('<html><body> deleting the activity')






class ActivityHandler(webapp2.RequestHandler):
	def get(self,product_id):
		self.response.out.write('<html><body>')
		
		# Get all the activities
		activity = db.GqlQuery("SELECT * "
				"FROM Activity "
				"WHERE ANCESTOR IS :1 "
				"ORDER BY date DESC LIMIT 10",
				baresniff_key())
		
		self.response.out.write(product_id)
                self.response.out.write('</body></html>')

	def put(self,product_id):
		self.response.out.write('<html><body>')
		
		# Get all the activities
		activity = db.GqlQuery("SELECT * "
				"FROM Activity "
				"WHERE ANCESTOR IS :1 "
				"ORDER BY date DESC LIMIT 10",
				baresniff_key())
		
		self.response.out.write(product_id)
		self.response.out.write('</body></html>')

	def delete(self,product_id):
		self.response.out.write('<html><body> deleting activity : <pre>')
		self.response.out.write(product_id)
		self.response.out.write('</pre></body></html>')


app = webapp2.WSGIApplication([('/', MainPage),
			       ('/baresniff',RootHandler),
			       ('/baresniff/activities',ActivitiesHandler),
			       ('/baresniff/activities/(\d+)',ActivityHandler)],
			       debug=True)
