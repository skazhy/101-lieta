from dbmodels import *
from markdown import *

def get_tt(key):
    md = Markdown()
    txt = TemplateText.all().filter('name_short = ', key)
    return md.convert(txt[0].content)
