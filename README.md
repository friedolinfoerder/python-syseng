System Engineering: Python
==========================

Members
-------
Friedolin Förder: ff026 
Leon Schröder: ls066
 
...

Profiling
---------

We have two profiling strategies:

* creating profiling snapshots at every push to the repository
* in detail profiling with tools like the [Flask Debug-toolbar](https://github.com/mgood/flask-debugtoolbar)

###Creating profiling snapshots

At every push to the repository the tests will be started in debug mode with profiling enabled.
So for every request there is the following profiling information: 

* a callstack as textfile, created with the module [cProfile](http://docs.python.org/2/library/profile.html#module-cProfile) and the [Stats](http://docs.python.org/2/library/profile.html#pstats.Stats) class
* the profile binary file, created with [ProfilerMiddleware](http://werkzeug.pocoo.org/docs/contrib/profiler/) from the [werkzeug](http://werkzeug.pocoo.org/) module
* a dot image, created with [Gprof2Dot](http://code.google.com/p/jrfonseca/wiki/Gprof2Dot)
* a [kcachegrind](http://kcachegrind.sourceforge.net/html/Home.html) file for later in detail profiling inspections

So the changes and the corresponding effects to the code can easily tracked by looking at performance profile files.
You can go the server and compare two versions in the repository. The folder structure is like this:

```
profiling
    2014-02-17_18:20:37
        GET.root.000738ms
            callstack.txt
            dot.png
            profile.kgrind
            profile.prof
        GET.user.002123ms
            callstack.txt
            dot.png
            profile.kgrind
            profile.prof
    2014-02-19_11:14:20
        GET.root.001099ms
            callstack.txt
            dot.png
            profile.kgrind
            profile.prof
        GET.user.003041ms
            callstack.txt
            dot.png
            profile.kgrind
            profile.prof
```

The script which processes the profiling and creates the files is the [profile.py](https://github.com/friedolinfoerder/python-syseng/blob/master/profile.py) script.

An example of a created dot.png file:

<p align='center'>
  <img src='http://friedolinfoerder.github.io/repos/python-syseng/images/dot.png' />
</p>

And the corresponding (relevant) content of the callstack file:

```
Wed Feb 19 11:14:21 2014    profiling/2014-02-19_11:14:20/GET.root.001099ms/profile.prof

         100330 function calls in 1.099 seconds

   Ordered by: internal time, function name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   100000    1.083    0.000    1.083    0.000 /home/friedolin/git/python-profiling/app.py:12(calculate)
        1    0.015    0.015    1.099    1.099 /home/friedolin/git/python-profiling/app.py:17(hello_world)
```

Here in this example you can see that the `calculate`-function takes almost all of the execution time.

###In detail profiling

Creating profiling snapshots is a good thing to see performance changes in your codebase, but this is not enough to fix serious performance problems. Therefore you should profile your code manually. We've take a look at the following tools for python:

* See profiling information for every request with [Flask Debug-toolbar](https://github.com/mgood/flask-debugtoolbar)
* Graphical view of the call map and call graph with [kcachegrind](http://kcachegrind.sourceforge.net/html/Home.html)
* Memory profiling with [Line Profiler](https://pypi.python.org/pypi/memory_profiler)

####Live profiling with the Flask Debug-toolbar

For the flask framework there is a very useful tool called Debug-toolbar. With this you can not only inspect the request variables, templates, configuration variables, logging but also the callstack of the creation of the visited page and a line profiler ([LineProfilerPanel-Plugin](https://pypi.python.org/pypi/Flask-DebugToolbar-LineProfilerPanel)) which highlights critical lines, as you can see in this minimal example:

<p align='center'>
  <img src='http://friedolinfoerder.github.io/repos/python-syseng/images/lineprofiler.png' />
</p>
This makes it very easy and comfortable to discover the internals of the application and find possible bugs and performance bottlenecks.

How you can use a line profiler for profiling memory usage is described in the chapter "Memory profiling".

####Using kcachegrind to visualize the calltree

To get a better understanding what's going within the application and to understand the flow and the performance impact of functions of your application, we used kcachegrind to visualize the call graph and the call map. To use kcachegrind you have to install it 

``` sh
sudo apt-get install kcachegrind
```

and convert the profile data to the right output format. We are doing this in the discribed automated profile creation process. The script `pyprof2calltree.py` provides all necessary tools to make the conversion. This is basicly how it works:

``` python
from pyprof2calltree import convert
convert('profile.prof', 'profile.kgrind')
```

With this file and kcachegrind you can visualize the profiling as the following screenshot illustrates:

<p align='center'>
  <img src='http://friedolinfoerder.github.io/repos/python-syseng/images/kcachegrind.png' />
</p>

kcachegrind is a great tool to actually use the profile data to improve the performance of the application. With it's various options and different visualizations you faster see the problems in your code.

####Memory profiling

You must install the python-dev package, the psutils module and the memory profiler module:

``` sh
sudo apt-get install python-dev
sudo pip install psutil
sudo pip install memory_profiler
```

Then you can annotate the function you want to inspect:

``` python
@profile
@app.route('/memory')
def xrange_vs_range():
    xr = xrange(2**16)
	r  = range(2**16)

	return str(len(r))
```

And with the additional script
``` python
from app import app

@profile
def profiling():
    app.test_client().get('/memory')

profiling()
```
and the additional setting `-m memory_profiler` when starting the python interpreter
``` sh
python -m memory_profiler profile_memory.py
```
we can trigger the memory profiling and get this result:

```
Filename: app.py

Line #    Mem usage    Increment   Line Contents
================================================
    24   15.523 MiB    0.000 MiB   @profile
    25                             @app.route('/memory')
    26                             def xrange_vs_range():
    27   15.527 MiB    0.004 MiB       xr = xrange(2**16)
    28   17.562 MiB    2.035 MiB   	r  = range(2**16)
    29                             
    30   17.562 MiB    0.000 MiB   	return len(r)


Filename: memory_profile.py

Line #    Mem usage    Increment   Line Contents
================================================
     3   15.156 MiB    0.000 MiB   @profile
     4                             def profiling():
     5                             	app.test_client().get('/memory')
```

This tool is perfect to find memory leaks in code handeling your requests. With the use of `app.test_client()` it works seamlessly with the flask framework.
