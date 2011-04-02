from google.appengine.api             import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext             import webapp
import models, views

class StuffMain(webapp.RequestHandler):
    def get(self):
        stuff_page = self.getStuff()
        # stuff_page = self.renderStuff()
        self.response.out.write(stuff_page)

    def getStuff(self):
        return self.renderStuff()
        stuff_page = memcache.get("stuff_page")
        if stuff_page is not None:
            return stuff_page
        else:
            stuff_page = self.renderStuff()
            memcache.add("stuff_page", stuff_page, 600)
            return stuff_page

    def renderStuff(self):
        # text = models.get_tt('stuff')
        t_path = 'templates/public-stufflist.html'
        stuff = models.get_all_stuff()
        return views.render_view(t_path, 'stufflist', stuff)

class StuffEntry(webapp.RequestHandler):
    def get(self, post, page=1):
        t_path = 'templates/public-stuffentry.html'
        stuff = models.get_stuff(int(post))
        logs = models.get_logs(int(page), int(post))
        stuff_entry = views.render_view(t_path, 'stuffentry', [stuff, logs])
        self.response.out.write(stuff_entry)

application = webapp.WSGIApplication([('/s/(\d+)/(\d+)', StuffEntry),
                                      ('/stuff', StuffMain),
                                      ('/s/(.*)', StuffEntry)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
