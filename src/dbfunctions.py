from dbmodels import *
from markdown import *
from settings import *
from datetime import timedelta

def get_tt(key):
    md = Markdown()
    txt = TemplateText.all().filter('name_short = ', key)
    return md.convert(txt[0].content)

def get_logs(display_date,page=1,stuff=-1):
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
        
        md = Markdown()
        for log in logs:
            log.display = md.convert(log.content)
            log.daynr = log.date - START_DT - timedelta(days=-1)
            if stuff != -1: 
                log.numbers.remove(stuff)
            if display_date == 'short':
                log.combo = log.date.strftime(LOG_DATE_SHORT)
            if display_date == 'full':
                log.combo = log.date.strftime(LOG_DATE)
        return [logs,older,newer,spacer]
        
def get_stuff(post):
    stuff = Stuff.all().filter('number = ',post).fetch(limit=1)
    stuff[0].percent = round((stuff[0].progress*100.0 / stuff[0].total),2)
    round(stuff[0].percent)
    return stuff[0]
        
def get_all_stuff():        
    stuff_query = Stuff.all().order('number')
    stuff = stuff_query.fetch(limit=101)
    for s in stuff:
        s.status = 'status_ns'
        if s.progress > 0:
            s.status = 'status_s' 
        if s.completed:
            s.status = 'status_c'
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
    for s in stuff:
        stuff = get_stuff(s)
        key = 'inc_'+str(s)
        inc = req.get(key)
        stuff.progress += int(inc)
        stuff.save()
