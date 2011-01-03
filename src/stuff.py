import os, math, datetime, dbfunctions
from markdown import *
from datetime import timedelta
from dbmodels import Stuff, Log
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class StuffMain(webapp.RequestHandler):
    def get(self):
        stuff_page = self.getStuff()
        self.response.out.write(stuff_page)

    def getStuff(self):
        stuff_page = memcache.get("stuff_page")
        if stuff_page is not None:
            return stuff_page
        else:
            stuff_page = self.renderStuff()
            memcache.add("stuff_page",stuff_page,600)
            return stuff_page
    
    def renderStuff(self):
        text = dbfunctions.get_tt('stuff')
        stuff_query = Stuff.all().order('number')
        stuff = stuff_query.fetch(limit=101)
        template_values = { 'stufflist':stuff,
                            'tt': text
                          }
        path = os.path.join(os.path.dirname(__file__), 'templates/public-stufflist.html')
        return template.render(path, template_values)

class StuffEntry(webapp.RequestHandler):
    def get(self, post):
		post = int(post)
		start_date = datetime.datetime(2010,10,11,0,0) 
		
		stuff_query = Stuff.all().filter('number = ', post)
		stuff = stuff_query.fetch(limit=1)
		for aStuff in stuff:
			aStuff.percent = round((aStuff.progress*100.0 / aStuff.total),2)
			round(aStuff.percent)
		log_query = Log.all().filter('number = ',post).order('-date')
		logs = log_query.fetch(limit=30)
	    md = Markdown()	
		for log in logs:
            log.display = md.convert(log.content)
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
