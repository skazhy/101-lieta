import os
from datetime import timedelta

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

from markdown import Markdown

import dbfunctions

class MainPage(webapp.RequestHandler):
    def get(self, page=1):
        if page == 1:
            # main_page = self.renderPage(1)
            main_page = self.getMain()
        else:
            main_page = self.renderPage(page)
        self.response.out.write(main_page)

    def getMain(self):
        main_page = memcache.get("main_page")
        if main_page is not None:
            return main_page
        else:
            main_page = self.renderPage(1)
            memcache.add("main_page",main_page,600)
            return main_page
    
    def renderPage(self, page):
        logs = dbfunctions.get_logs('short', int(page))
        template_values = {
            'logs': logs[0],
            'older': logs[1],
            'newer': logs[2],
            'spacer': logs[3],
        }
        path = os.path.join(os.path.dirname(__file__),'templates/public-logs.html')
        main_page = template.render(path,template_values)
        return main_page

application = webapp.WSGIApplication([('/', MainPage), ('/l/(.*)',MainPage)],debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
