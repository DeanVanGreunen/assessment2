from html import escape

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    return dict()