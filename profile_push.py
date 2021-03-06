#!flask/bin/python

"""
File for profiling at every push to the repository.
Profiling snapshots of the app will be generated by this script.

@author Friedolin Förder
@author Leon Schröder
"""

from werkzeug.contrib.profiler import ProfilerMiddleware, MergeStream
import sys
from app import app
import os
import subprocess
import shutil
import pstats
import StringIO
from pyprof2calltree import convert, visualize
import datetime

# create timestamp
now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

profile_dir = 'profiling'
now_dir = profile_dir + '/' + now
temp_dir = 'temp'

if not os.path.exists(profile_dir):
    os.mkdir(profile_dir)

os.mkdir(now_dir)
os.mkdir(temp_dir)

app.config['PROFILE'] = True
f = open('profiler.log', 'w')
stream = MergeStream(sys.stdout, f)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [50], stream=stream, profile_dir=temp_dir)

# define requests for profiling and create profile data
app.test_client().get('/')
app.test_client().get('/user')
app.test_client().get('/user/1')


for file_name in os.listdir(temp_dir):
    name = '.'.join(file_name.split('.')[:-2])
    request_dir = os.path.join(now_dir, name)
    os.mkdir(request_dir)
    old_file_path = os.path.join(temp_dir, file_name)
    new_file_path = os.path.join(request_dir, 'profile.prof')
    os.rename(old_file_path, new_file_path)

    txt_path = os.path.join(request_dir, 'callstack.txt')
    kcachegrind_path = os.path.join(request_dir, 'profile.kgrind')
    png_path = os.path.join(request_dir, 'dot.png')

    # create text file
    stream = StringIO.StringIO()
    stats = pstats.Stats(new_file_path, stream=stream)
    stats = stats.sort_stats("time", "name")
    stats.print_stats()
    with open(txt_path, 'w') as f:
        f.write(stream.getvalue())

    # create kcachegrind file
    convert(new_file_path, kcachegrind_path)

    # create png
    subprocess.call('./gprof2dot.py -f pstats %s | dot -Tpng -o %s' % (new_file_path,png_path), shell=True)

os.rmdir(temp_dir)