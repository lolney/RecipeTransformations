import cherrypy
from src.web.cherrpy_root import Root

cherrypy.quickstart(Root())