import os, math, datetime, dbfunctions
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class StuffMain(webapp.RequestHandler):
    def get(self):
        # stuff_page = self.getStuff()
        stuff_page = self.renderStuff()
        self.response.out.write(stuff_page)

    def getStuff(self):
        return self.renderStuff()
        stuff_page = memcache.get("stuff_page")
        if stuff_page is not None:
            return stuff_page
        else:
            stuff_page = self.renderStuff()
            memcache.add("stuff_page",stuff_page,600)
            return stuff_page
    
    def renderStuff(self):
        # text = dbfunctions.get_tt('stuff')
        t_path = 'templates/public-stufflist.html'
        stuff = dbfunctions.get_all_stuff()
        template_values = { 
            'stufflist':stuff,
        }
        path = os.path.join(os.path.dirname(__file__), t_path)
        return template.render(path, template_values)

class StuffEntry(webapp.RequestHandler):
    def get(self, post, page=1):
        t_path = 'templates/public-stuffentry.html'
        stuff = dbfunctions.get_stuff(int(post))
        logs = dbfunctions.get_logs(int(page),int(post))
        template_values = {
            'stuff':stuff,
            'logs': logs[0],
            'older': logs[1],
            'newer': logs[2],
            'spacer': logs[3],
        }
        path = os.path.join(os.path.dirname(__file__), t_path)
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/s/(\d+)/(\d+)', StuffEntry),
                                      ('/stuff', StuffMain),
                                      ('/s/(.*)', StuffEntry)],
                                     debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
