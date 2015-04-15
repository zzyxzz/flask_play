from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask_flatpages import FlatPages, pygments_style_defs, pygmented_markdown
import collections

FLATPAGES_EXTENSION = ".md"
FLATPAGES_ROOT = "content"
POSTS_DIR = "posts"

app = Flask(__name__)
bootstrap = Bootstrap(app)
flatpages = FlatPages(app)
app.config.from_object(__name__)
post_list = []

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

@app.route("/about")
def aboutme():
	return render_template("about.html")

@app.route("/static/css/pygments.css")
def pygments_css():
	return pygments_style_defs("tango"), 200, {"Content-Type":"text/css"}

#===========
if __name__ == "__main__":
	app.run(host="0.0.0.0")
