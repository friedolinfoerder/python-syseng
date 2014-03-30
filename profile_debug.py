#!/usr/bin/env python

"""
File for live profiling.
Go to a page and you will see the Flask Debug-toolbar.

@author Friedolin Förder
@author Leon Schröder
"""

from flask import *
from flask_debugtoolbar import DebugToolbarExtension
from dozer import Dozer
from app import app

'''
import types
def copy_func(f, name=None):
    return types.FunctionType(f.func_code, f.func_globals, name or f.func_name,
        f.func_defaults, f.func_closure)

for i, rule in enumerate(list(app.url_map.iter_rules())):
    url = str(rule)
    if url[:2] != '/_':
        def define(uri):
            def f():
                print uri
                with app.test_client() as client:
                    response = client.get(uri)
                    return Response('<body>'+response.data+'</body>')

            setattr(globals, 'dynamic_uri_'+str(i), copy_func(f, '/debug' + uri))
            app.route('/debug' + uri)(getattr(globals, 'dynamic_uri_'+str(i)))
        define(url)
'''

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['DEBUG_TB_PROFILER_ENABLED'] = True
# Specify the debug panels you want
app.config['DEBUG_TB_PANELS'] = [
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    # Add the line profiling
    'flask_debugtoolbar_lineprofilerpanel.panels.LineProfilerPanel'
]

toolbar = DebugToolbarExtension(app)
#dozer = Dozer(app)
    
app.run()
