import re
import threading 
request_cfg = threading.local()

#https://stackoverflow.com/questions/27401779/dynamically-set-database-based-on-request-in-django

# #intercepts requests
class SimpleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # pattern = re.compile("\\b(http://|https://|www.|.com|8000|:|//)\\W\\d+", re.I)
        # words = request.get_host()        
        # db_name = [pattern.sub("", words)][0].split('.')[0]

        #crappy just for testing......
        db_name = request.build_absolute_uri().split('//')[1]
        db_name = db_name.split('/')[1]

        if db_name == "polls":
            db_name = "sql1"
        elif db_name == "polls2":
            db_name = "sql2"
        else: 
            db_name = None

            
        request_cfg.cfg = db_name

        response = self.get_response(request)

        if hasattr( request_cfg, 'cfg' ):
            del request_cfg.cfg

        return response


#routing for database depending on request.
class DatabaseRouter (object):
    def _default_db( self ):
        if hasattr( request_cfg, 'cfg' ):
            return request_cfg.cfg
        else:
            return 'default'

    def db_for_read( self, model, **hints ):
        return self._default_db()

    def db_for_write( self, model, **hints ):
        return self._default_db()