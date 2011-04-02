from google.appengine.ext import db

from datetime import timedelta

from settings import *

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

def get_tt(key):
    txt = TemplateText.all().filter('name_short = ', key)
    return txt[0].content

def get_all_tt():
    tt = TemplateText.all()
    return tt


def get_logs(page=1,stuff=-1):
        older = False
        newer = False
        spacer = False
        offset = page*EPP-EPP

        log_query = Log.all()
        if stuff == -1:
            log_query.order('-date')
        else:
            log_query.filter('numbers = ',stuff).order('-date')
        logs = log_query.fetch(limit = EPP+1, offset = offset)
        if len(logs) == EPP+1:
            p_new = str(page + 1)
            older = '/l/' + p_new
            if stuff != -1:
                older = '/s/' + str(stuff) + '/' + p_new
            logs.pop()
        if offset > 0:
            p_new = str(page - 1)
            newer = '/l/' + p_new
            if stuff != -1 and page == 2:
                newer = '/s/' + str(stuff)
            if stuff != -1 and page != 2:
                newer = '/s/'+ str(stuff) + '/' + p_new
            if stuff == -1 and page == 2:
                newer = '/'
        if len(logs) == 0:
            older=newer=False
        if newer and older:
            spacer = True

        for log in logs:
            log.daynr = log.date - START_DT - timedelta(days=-1)
            if stuff != -1:
                log.numbers.remove(stuff)
        return [logs,older,newer,spacer]

def get_log(post):
    return Log.get_by_id(post)

def get_stuff(post):
    if post != 0:
        stuff = Stuff.all().filter('number = ',post).fetch(limit=1)
        stuff[0].percent = round((stuff[0].progress*100.0 / stuff[0].total),2)
        round(stuff[0].percent)
        return stuff[0]
    else:
        return False

def get_all_stuff():
    stuff_query = Stuff.all().order('number')
    stuff = stuff_query.fetch(limit=101)
    for s in stuff:
        s.status = 'ns'
        if s.progress > 0:
            s.status = 's'
        if s.completed:
            s.status = 'c'
    return stuff

def save_log(req, mode='edit'):
    if mode == 'edit':
        log = db.get(req.get('id'))
    if mode == 'new':
        log = Log()
        log.date = datetime.datetime.now() + timedelta(hours=UTCDIFF)

    str_numbers = req.get('number').split(' ')
    log.numbers=[]
    for n in str_numbers:
        log.numbers.append(int(n))
    log.numbers.sort()
    log.content = req.get('content')
    db.put(log)

def save_stuff(req, mode='edit'):
    if mode == 'edit':
        stuff = db.get(req.get('id'))
    if mode == 'new':
        stuff = Stuff()
        stuff.number = int(req.get('number'))
    stuff.content = req.get('content')
    stuff.progress = int(req.get('progress'))
    stuff.total = int(req.get('total'))
    if stuff.progress >= stuff.total:
        stuff.completed = True
    else:
        stuff.completed = False
    db.put(stuff)

def save_increment(req):
    stuff = []
    for r in req.arguments():
        if r[:4] == 'inc_':
            stuff.append(int(r[4:]))
    if 0 in stuff:
        stuff.remove(0)
    for s in stuff:
        stuff = get_stuff(s)
        key = 'inc_'+str(s)
        inc = req.get(key)
        stuff.progress += int(inc)
        if stuff.progress >= stuff.total:
            stuff.completed = True
        stuff.save()

def save_tt(req,mode):
    if mode == 'edit':
        tt = db.get(req.get('name_short'))
    if mode == 'new':
        tt = TemplateText()
        tt.name_short = req.get('name_short')
    tt.content = req.get('content')
    db.put(tt)
