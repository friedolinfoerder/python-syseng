#!/usr/bin/env python

"""
File for memory profiling.
Choose the page to profile and set the profile decorator in the app.

@author Friedolin Förder
@author Leon Schröder
"""

from app import app

@profile
def profiling():
    app.test_client().get('/memory')

profiling()