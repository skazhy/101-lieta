from google.appengine.ext.webapp import template
import os
from markdown import Markdown

def render_view(t_path, view='static', values=None):
    template_values={}
    if view == 'logs':
        md = Markdown()
        for log in values[0]:
            log.display = md.convert(log.content)
        template_values = {
            'logs': values[0],
            'older': values[1],
            'newer': values[2],
            'spacer': values[3],
        }

    if view == 'stufflist':
        template_values = {
            'stufflist':values,
    }
    if view == 'logentry':
        template_values = {
            'log':values,
    }
    if view == 'stuffentry':
        md = Markdown()
        for log in values[1][0]:
            log.display = md.convert(log.content)
        template_values = {
            'stuff':values[0],
            'logs': values[1][0],
            'older': values[1][1],
            'newer': values[1][2],
            'spacer': values[1][3],
        }
    if view == 'info':
        md = Markdown()
        conv_info = md.convert(values)
        template_values = {'tt': conv_info }

    if view == 'editlogs':
        template_values = {'logs': values}

    if view == 'editstuff':
        template_values = {'stufflist': values}

    if view == 'edittt':
        template_values = {'tt': values}

    path = os.path.join(os.path.dirname(__file__),t_path)
    return template.render(path,template_values)
