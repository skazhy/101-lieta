import cgi,datetime, os
from dbmodels import *

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class AdminMain(webapp.RequestHandler):
    def get(self):
        if users.is_current_user_admin():
        	path = os.path.join(os.path.dirname(__file__), 'templates/base-admin.html')
        	self.response.out.write(template.render(path, {}))
        else:
			self.redirect('/')

# displaying edit forms
class EditEntry(webapp.RequestHandler):
    def get(self,mode):
        if users.is_current_user_admin():
			template_values = {}
			if mode == "log":
				logs = db.GqlQuery("SELECT * FROM Log ORDER BY date DESC LIMIT 5")
				template_values = {'logs' : logs}
			if mode == "stuff":
				stufflist = db.GqlQuery("SELECT * FROM Stuff ORDER BY number ASC")
				template_values = {'stufflist' : stufflist}
			path = os.path.join(os.path.dirname(__file__), 'templates/admin-edit.html')
			self.response.out.write(template.render(path, template_values))
        else:
			self.redirect('/')

class WriteLog(webapp.RequestHandler):
    def post(self):
    	if users.is_current_user_admin():
			counter = int(self.request.get('counter'))
			logToEdit = db.GqlQuery("SELECT * FROM Log ORDER BY date DESC")
			result = logToEdit.fetch(counter+1)
			result[-1].number = int(self.request.get('number'))
			result[-1].content = self.request.get('content')
			db.put(result)	
			self.redirect('/admin/edit_log')
        else:
			self.redirect('/')
	
# editing existing entry
class WriteStuff(webapp.RequestHandler):
    def post(self):
    	if users.is_current_user_admin():
			number = int(self.request.get('stuffnumber'))
			stuffToEdit = db.GqlQuery("SELECT * FROM Stuff WHERE number = %s LIMIT 1" % number)
			result = stuffToEdit.get()
			result.content = self.request.get('stuffcontent')
			result.progress  = int(self.request.get('stuffprogress'))
			result.total  = int(self.request.get('stufftotal'))
			result.completed = False
			if(result.total <= result.progress):
				result.completed = True
			db.put(result)	
			self.redirect('/admin/edit_stuff')
        else:
			self.redirect('/')

# adding new entry from admin main
class PostEntry(webapp.RequestHandler):
    def post(self, mode):
    	if users.is_current_user_admin():
			if mode == "stuff":
				stuff = Stuff()
				stuff.number = int(self.request.get('number'))
				stuff.content = self.request.get('content')
				stuff.progress = int(self.request.get('progress'))
				stuff.total = int(self.request.get('total'))
				if stuff.progress >= stuff.total:
					stuff.completed = False
				else:
					stuff.completed = False
				stuff.put()
			if mode == "log":
				log = Log()
				log.content = self.request.get('content')
				log.number = int(self.request.get('number'))
				log.date = datetime.datetime.now()
				log.put()
			self.redirect('/admin')
        else:
			self.redirect('/')

application = webapp.WSGIApplication([('/admin', AdminMain),('/admin/edit_(.*)',EditEntry),('/admin/post_(.*)',PostEntry),
									('/admin/writes',WriteStuff),('/admin/writel',WriteLog)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
