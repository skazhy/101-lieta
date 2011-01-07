import os, datetime
from markdown import *
from datetime import timedelta
from dbmodels import Log
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from settings import *

class LogPage(webapp.RequestHandler):
    def get(self,page=1):
        start_dt = datetime.datetime(S_YEAR, S_MONTH, S_DAY, 0, 0)
        print start_dt
        page = int(page)
        older = newer = False
        offset = page*EPP-EPP

        logs_query = Log.all().order('-date')
        logs = logs_query.fetch(limit = EPP+1, offset = offset)
        
        if len(logs) == EPP+1:
            older = page+1
            logs.pop()
        if offset > 0:
            newer = page-1
        if len(logs) == 0:
            older=newer=False
        
        md = Markdown()
        for log in logs:
            log.display = md.convert(log.content)
            log.daynr = log.date - start_dt - timedelta(days=-1)
            log.combo = log.date.strftime(LOG_DATE)
        
        template_values = {
            'logs':logs,
            'older':older,
            'newer':newer
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/public-logs.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/logs', LogPage),('/logs/(.*)', LogPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
