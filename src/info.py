import os
import dbfunctions
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Info(webapp.RequestHandler):
    def get(self):
        text = dbfunctions.get_tt('info')
        path = os.path.join(os.path.dirname(__file__), 'templates/public-info.html')
        template_values = {'tt': text }
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/info',Info)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
    
