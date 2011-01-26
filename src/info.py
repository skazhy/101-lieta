from google.appengine.ext             import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, views

class Info(webapp.RequestHandler):
    def get(self):
        text = models.get_tt('info')
        t_path = 'templates/public-info.html'
        info_page = views.render_view(t_path, 'info', text)
        self.response.out.write(info_page)

application = webapp.WSGIApplication([('/info', Info)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
    
