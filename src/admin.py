from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users, memcache
import cgi
import os
import dbfunctions
from dbmodels import *
from settings import *


class AdminMain(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/base-admin.html')
        self.response.out.write(template.render(path, {}))
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
                logs = dbfunctions.get_logs(1)
                for log in logs[0]:
                    log.numb = ''
                    for n in log.numbers:
                        log.numb += str(n) + ' '
                    log.numb = log.numb[:-1]
                template_values = {'logs': logs[0]}
            if mode == "stuff":
                stuff = dbfunctions.get_stuff()
                template_values = {'stufflist': stufflist}
            if mode == "ttext":
                tt = db.GqlQuery("SELECT * FROM TemplateText")
                template_values = {'tt' : tt}
            
            path = os.path.join(os.path.dirname(__file__), 'templates/admin-edit.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/')

# editing existing entry
class WriteLog(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            dbfunctions.save_log(self.request)
            memcache.delete('main_page')
            self.redirect('/admin/edit_log')
        else:
            self.redirect('/')
class WriteStuff(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            memcache.delete('stuff_page')
            self.redirect('/admin/edit_stuff')
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
    
# adding new entry from admin main
class PostEntry(webapp.RequestHandler):
    def post(self, mode):
        if users.is_current_user_admin():
            if mode == "log":
                dbfunctions.save_log(self.request,'new')
                memcache.delete('main_page')
            if mode == "stuff":
                dbfunctions.save_stuff(self.request,'new')
                memcache.delete('stuff_page')
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
