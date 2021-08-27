from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


from views import home_view

def hello_world(request):
    return Response('Hello World!')


if __name__ == '__main__':
    with Configurator() as config:
        config.include("pyramid_jinja2") # include jinga2 template processing
        config.add_renderer('.jinja2', 'pyramid_jinja2.renderer_factory') # align jinja2 files to be processed by the jinga2 template factory/processor
        config.add_route('home', '/') # register home view, all ui and apis are on client side
        config.scan('views')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 80, app)
    server.serve_forever()