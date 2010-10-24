import os, math
import datetime
from datetime import timedelta
from dbmodels import Stuff
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Stats(webapp.RequestHandler):
    def get(self):
		# laiku apreekjins
		saakums = datetime.datetime(2010,10,11,0,0)
		tagad = datetime.datetime.now()
		diffDone = tagad - saakums
		diffCurrent = diffDone - timedelta(days=-1)

		#izpildiitaa apreekjins
		query = Stuff.all()
		query.filter('completed = ', True)
		completed = query.fetch(limit=101)
		ccount = len(completed)	
	
		query = Stuff.all()
		query.filter('progress > ', 0)
		started = query.fetch(limit=101)
		scount = len(completed)	
		
		#prochi
		stuffperday =  round(1/round((diffCurrent.days/ccount),5),5)
		path = os.path.join(os.path.dirname(__file__), 'pub-stats.html')
		template_values = {
			'daysDone':diffDone.days,
			'daysCurr':diffCurrent.days,
			'completed':ccount,
			'started':scount,
			'stuffperday':stuffperday,
		}
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/stats', Stats)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
