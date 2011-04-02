from google.appengine.ext             import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api             import users, memcache
import models, views

class AdminMain(webapp.RequestHandler):
    def get(self):
        if users.is_current_user_admin():
            t_path = 'templates/admin-add.html'
            admin_main = views.render_view(t_path)
            self.response.out.write(admin_main)
        else:
            self.redirect('/')

# displaying edit forms
class EditEntry(webapp.RequestHandler):
    def get(self,mode):
        if users.is_current_user_admin():
            if mode == "log":
                t_path = 'templates/admin-editlogs.html'
                logs = models.get_logs()
                page = views.render_view(t_path, 'editlogs',logs[0])
            if mode == "stuff":
                t_path = 'templates/admin-editstuff.html'
                stuff = models.get_all_stuff()
                page = views.render_view(t_path, 'editstuff', stuff)
            if mode == "ttext":
                t_path = 'templates/admin-edittt.html'
                tt = models.get_all_tt()
                page = views.render_view(t_path, 'edittt', tt)
            self.response.out.write(page)
        else:
            self.redirect('/')

# editing existing entry
class WriteLog(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            models.save_log(self.request)
            memcache.delete('main_page')
            self.redirect('/admin/edit_log')
        else:
            self.redirect('/')
class WriteStuff(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            models.save_stuff(self.request)
            memcache.delete('stuff_page')
            self.redirect('/admin/edit_stuff')
        else:
            self.redirect('/')
class WriteTtext(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            models.save_tt(self.request,'edit')
            self.redirect('/admin/edit_ttext')
        else:
            self.redirect('/')

# adding new entry from admin main
class PostEntry(webapp.RequestHandler):
    def post(self, mode):
        if users.is_current_user_admin():
            if mode == "log":
                models.save_log(self.request,'new')
                models.save_increment(self.request)
                memcache.delete('main_page')
            if mode == "stuff":
                models.save_stuff(self.request,'new')
                memcache.delete('stuff_page')
            if mode == "ttext":
                ttext = models.save_tt(self.request,'new')
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
