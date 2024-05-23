from flask import Flask, url_for, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/bye")
def bye_world():
    return "<p>Bye, World!</p>"


@app.route("/hello/<username>")
def helo_user(username):
    return render_template('helo_user_html', username=username)


@app.route('/posts')
def posts():
    return render_template('posts.html', posts=range(1, 11))


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    return render_template('show_post.html', post_id=post_id)


@app.route('/login')
def login():
    return 'login'


@app.route('/profile')
def profile():
    template = '<a href="{}">User {}</a>'
    return '<br>'.join([
        template.format(url_for('show_post', post_id=i), i) for i in range(1, 11, 1)
    ])
