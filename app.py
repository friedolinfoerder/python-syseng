
from flask import *
from cProfile import Profile
app = Flask(__name__)
from flask_debugtoolbar_lineprofilerpanel.profile import line_profile

def to_html(result):
	def func():
		r = result()
		return '<body>'+r+'</body>'
	return func

def calculate(i):
	while(i > 0.001):
		i /= 1.1
	return i

@app.route('/')
@to_html
def hello_world():
	for i in range(1000):
		calculate(i)
	return 'Hello World!'

@app.route('/memory')
@line_profile
def xrange_vs_range():
	xr = xrange(2**16)
	r  = range(2**16)

	return '<body>%s</body>' % (str(len(r)),)

@app.route('/user')
def hello_user():
    return 'Hello User!'

@app.route('/user/1')
def hello_user_1():
    return 'Hello User 1!'


if __name__ == '__main__':
    #app.run()
    app.test_client().get('/')
    app.test_client().get('/user')