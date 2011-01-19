from google.appengine.ext import db

class Stuff(db.Model):
	number = db.IntegerProperty()
	content = db.StringProperty()
	completed = db.BooleanProperty()
	progress = db.IntegerProperty()
	total = db.IntegerProperty()

class Log(db.Model):
	number = db.IntegerProperty()
	numbers = db.ListProperty(int)
	content = db.TextProperty()
	date = db.DateTimeProperty()

class TemplateText(db.Model):
    name_short = db.StringProperty()
    content = db.TextProperty()
