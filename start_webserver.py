import cherrypy, os
from recipetransform.web.cherrpy_root import Root

conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './templates'
         }
     }
cherrypy.quickstart(Root(), '/', conf)