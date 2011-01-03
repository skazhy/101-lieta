import cgi
import datetime
import os

from dbmodels import *
from datetime import timedelta 

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users, memcache

class AdminMain(webapp.RequestHandler):
    def get(self):
        if users.is_current_user_admin():
            path = os.path.join(os.path.dirname(__file__), 'templates/base-admin.html')
            self.response.out.write(template.render(path, {}))
        else:
            self.redirect('/')

# displaying edit forms
class EditEntry(webapp.RequestHandler):
    def get(self,mode):
        if users.is_current_user_admin():
            template_values = {}
            if mode == "log":
                logs = db.GqlQuery("SELECT * FROM Log ORDER BY date DESC LIMIT 5")
                template_values = {'logs' : logs}
            if mode == "stuff":
                stufflist = db.GqlQuery("SELECT * FROM Stuff ORDER BY number ASC")
                template_values = {'stufflist' : stufflist}
            if mode == "ttext":
                tt = db.GqlQuery("SELECT * FROM TemplateText")
                template_values = {'tt' : tt}
            
            path = os.path.join(os.path.dirname(__file__), 'templates/admin-edit.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/')

class WriteLog(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            log = db.get(self.request.get('id'))
            log.number = int(self.request.get('number'))
            log.content = self.request.get('content')
            db.put(log)    
            self.redirect('/admin/edit_log')
        else:
            self.redirect('/')

class WriteTtext(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            ttext = db.get(self.request.get('name_short'))
            ttext.content = self.request.get('content')
            db.put(ttext)    
            self.redirect('/admin/edit_ttext')
        else:
            self.redirect('/')
    
# editing existing entry
class WriteStuff(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            stuff = db.get(self.request.get('id'))
            stuff.content = self.request.get('stuffcontent')
            stuff.progress  = int(self.request.get('stuffprogress'))
            stuff.total  = int(self.request.get('stufftotal'))
            stuff.completed = False
            if(stuff.total <= stuff.progress):
                stuff.completed = True
            memcache.delete('main_page')
            memcache.delete('stuff_page')
            db.put(stuff)
            self.redirect('/admin/edit_stuff')
        else:
            self.redirect('/')

# adding new entry from admin main
class PostEntry(webapp.RequestHandler):
    def post(self, mode):
        if users.is_current_user_admin():
            # Difference from UTF time.
            td = timedelta(hours=2)
            
            if mode == "stuff":
                stuff = Stuff()
                stuff.number = int(self.request.get('number'))
                stuff.content = self.request.get('content')
                stuff.progress = int(self.request.get('progress'))
                stuff.total = int(self.request.get('total'))
                if stuff.progress >= stuff.total:
                    stuff.completed = False
                else:
                    stuff.completed = False
                memcache.delete('stuff_page')
                stuff.put()
            if mode == "log":
                log = Log()
                log.date = datetime.datetime.now() + td
                log.content = self.request.get('content')
                log.number = int(self.request.get('number'))
                log.put()
            if mode == "ttext":
                ttext = TemplateText()
                ttext.content = self.request.get('content')
                ttext.name_short = self.request.get('name_short')
                ttext.put()
            self.redirect('/admin')
        else:
            self.redirect('/')

application = webapp.WSGIApplication([('/admin', AdminMain),
                                      ('/admin/edit_(.*)',EditEntry),
                                      ('/admin/post_(.*)',PostEntry),
                                      ('/admin/writes',WriteStuff),
                                      ('/admin/writet',WriteTtext),
                                      ('/admin/writel',WriteLog)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
