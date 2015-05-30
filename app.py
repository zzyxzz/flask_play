from flask import Flask, render_template, flash, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask_flatpages import FlatPages, pygments_style_defs, pygmented_markdown
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required
import os

FLATPAGES_EXTENSION = ".md"
FLATPAGES_ROOT = "content"
POSTS_DIR = "posts"
# for pagination
TABLE_PER_PAGE = 10
SECRET_KEY = "Never cracked"

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
flatpages = FlatPages(app)
app.config.from_object(__name__)
post_list = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 't2_data.sqlite')
app.config['SQLAlchemy_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

"""
Define models according to the table in csv file 
for import data from csv file or furthur database manipulations.
"""

subs = db.Table('subs',
	db.Column('org_id', db.Integer, db.ForeignKey('organisations.id')),
	db.Column('sub_tier_id', db.Integer, db.ForeignKey('subtiers.id')))

class Organisation(db.Model):
	__tablename__ = 'organisations'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80))
	town_id = db.Column(db.Integer, db.ForeignKey('towns.id'))
	sub_tiers = db.relationship('SubTier', secondary = subs, 
		backref=db.backref('organisations',lazy='dynamic'))
	# sub_tier_id = db.Column(db.Integer, db.ForeignKey('subtiers.id'))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Organisation %r>' % self.name

class Town(db.Model):
	__tablename__ = 'towns'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), unique = True)
	county_id = db.Column(db.Integer, db.ForeignKey('counties.id'))
	organisations = db.relationship('Organisation', backref = 'town', lazy = 'dynamic')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Town %r>' % self.name

class County(db.Model):
	__tablename__ = 'counties'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), unique = True)
	towns = db.relationship('Town', backref = 'county', lazy = 'dynamic')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<County %r>' % self.name

class Tier(db.Model):
	__tablename__ = 'tiers'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), unique = True)
	sub_tiers = db.relationship('SubTier', backref = 'tier', lazy = 'dynamic')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Tier %r>' % self.name

class SubTier(db.Model):
	__tablename__ = 'subtiers'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), unique = True)
	tier_id = db.Column(db.Integer, db.ForeignKey('tiers.id'))
	# organisations = db.relationship('Organisation', backref = 'subtier', lazy = 'dynamic')

	def __init__(self, name):
		self.name = name
		
	def __repr__(self):
		return '<Sub Tier %r>' % self.name

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/posts")
def list_posts():
	post_list[:] = [post for post in flatpages if post.path.startswith(POSTS_DIR)]
	post_list.sort(key=lambda p: p['published'], reverse=True)
	if not post_list:
		return render_template("index.html")
	return render_template("posts.html",post_list=post_list)

@app.route("/posts/<name>")
def show_post(name):
	path = "{}/{}".format(POSTS_DIR, name)
	post = flatpages.get_or_404(path)
	p_index = post_list.index(post)
	pre_page = None
	next_page = None
	if 0 < p_index:
		pre_page = post_list[p_index-1]
	if p_index <len( post_list)-1:
		next_page = post_list[p_index+1]
	return render_template("post.html",post=post, pre_page=pre_page, next_page=next_page)

@app.route("/sponsorship", methods = ['GET','POST'])
@app.route("/sponsorship/<int:page>", methods = ['GET','POST'])
def show_table(page = 1):
	sponsor_list = Organisation.query.paginate(page, TABLE_PER_PAGE)
	max_n = sponsor_list.total
	pages = sponsor_list.pages
	num = None
	goto = numeric_form()
	if goto.validate_on_submit():
		num = goto.num.data
		if 1 <= num and num <= pages:
			goto.num.data = ''
			return redirect(url_for('show_table', page = num))
		else:
			flash('Page number is out of range.')

	return render_template("table.html", sponsor_list = sponsor_list, goto = goto, max_n = max_n, title = "Tier 2 List")

@app.route("/about")
def aboutme():
	return render_template("about.html")

@app.route("/static/css/pygments.css")
def pygments_css():
	return pygments_style_defs("tango"), 200, {"Content-Type":"text/css"}

class numeric_form(Form):
	num = IntegerField('Go to', validators=[Required()])
	submit = SubmitField('Go')

#===========
if __name__ == "__main__":
	host = '0.0.0.0'
	debug = True
	app.run(host=host)
