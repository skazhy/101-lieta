import os, math, datetime
from datetime import timedelta
from dbmodels import Stuff, Log
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class StuffMain(webapp.RequestHandler):
    def get(self):
		query = Stuff.all().order('number')
		stuff = query.fetch(limit=101)
		
		template_values = {
			'stufflist':stuff
		}
		
		path = os.path.join(os.path.dirname(__file__), 'templates/public-stufflist.html')
		self.response.out.write(template.render(path, template_values))

class StuffEntry(webapp.RequestHandler):
    def get(self, post):
		post = int(post)
		start_date = datetime.datetime(2010,10,11,0,0) 
		
		stuff_query = Stuff.all().filter('number = ', post)
		stuff = stuff_query.fetch(limit=1)
		
		stuff[-1].percent = round((stuff[-1].progress*100.0 / stuff[-1].total),2)
		round(stuff[-1].percent)
		
		log_query = Log.all().filter('number = ',post).order('-date')
		logs = log_query.fetch(limit=30)
		
		for log in logs:
			log.daynr = diffCurrent = log.date - start_date - timedelta(days=-1)
			log.combo = log.date.strftime("%H:%M, %d-%m-%Y")	
		
		template_values = {
			'stuff':stuff,
			'logs':logs
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/public-stuffentry.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/s/(.*)', StuffEntry),('/stuff', StuffMain)],
                                     debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
