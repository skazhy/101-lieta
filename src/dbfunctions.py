from dbmodels import *

def get_tt(key):
    txt = TemplateText.all().filter('name_short = ', key)
    return txt[0].content
