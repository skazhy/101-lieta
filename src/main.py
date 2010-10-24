import os
import datetime
from datetime import timedelta
from dbmodels import Stuff
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
		start_date = datetime.datetime(2010,10,11,0,0)
		todays_date = datetime.datetime.now()
		done_days = todays_date - start_date
		day_percent = int(done_days.days*100/1001)
		current_day = done_days - timedelta(days=-1)
		
		task_query = Stuff.all().filter('completed = ', True)
		completed = task_query.fetch(limit=101)
		comp_count = len(completed)	
		task_percent = int(comp_count*100/101)	
		
		task_query = Stuff.all().filter('progress > ', 0)
		started = task_query.fetch(limit=101)
		started_count = len(started)
		task_percent = int(comp_count*100/101)	
		
		template_values = {
			'current_day':current_day.days,
			'day_percent':day_percent,
			'task_percent':task_percent,
			'started':started_count,
			'completed':comp_count
		}
		
		path = os.path.join(os.path.dirname(__file__), 'templates/base-public.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', MainPage)],debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
