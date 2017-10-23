from flask import Flask, render_template, abort
from credentials.views import DashboardView
from auth.views import Index, AuthBackend, Logout
from pymongo import MongoClient
from utils.utils import RedisSession

import random, os, string

app = Flask(__name__)

app.config.from_object('config.config.DevelopmentConfig')
app.config['SECRET_KEY'] = 'dirac'
app.jinja_env.globals['STATIC_PREFIX'] = '/static/'

conn = MongoClient(os.environ['MONGODB_URI'])
db = conn[os.environ['MONGODB_DB']]

rsession = RedisSession()

@app.route('/500')
def gen_error():
	abort(500)


@app.errorhandler(404)
def not_found(e):
	return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html')

app.add_url_rule('/', view_func=Index.as_view('index', template_name='index.html', rsession=rsession))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard', template_name='dashboard.html', db=db, rsession=rsession))
app.add_url_rule('/auth', view_func=AuthBackend.as_view('auth', db=db, rsession=rsession))
app.add_url_rule('/logout', view_func=Logout.as_view('logout', rsession=rsession))

def main():
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])

if __name__ == '__main__':
    main()
