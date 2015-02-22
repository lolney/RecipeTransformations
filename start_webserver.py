import cherrypy
from recipetransform.web.cherrpy_root import Root

cherrypy.quickstart(Root())