from google.appengine.ext             import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api             import memcache

import models
import views

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
        logs = models.get_logs('short', int(page))
        t_path = 'templates/public-logs.html'
        return views.render_view(t_path, 'logs',logs)

application = webapp.WSGIApplication([('/', MainPage), ('/l/(.*)',MainPage)],debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
