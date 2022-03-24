from datetime import datetime

import logging

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

obj = Flask(__name__)
obj.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
obj.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(obj)

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Info %r>' % self.id


@obj.route("/")
@obj.route("/home")
def index():

    for i in range(379, 1, 1000):
        title = "Post title %r" % i
        intro = "Post intro %r" % i
        text = "Post description %r" % i

        info = Info(title=title, intro=intro, text=text)

        try:
            db.session.add(info)
            db.session.commit()
            logging.info("Inserted %r" % i)
        except:
            logging.info("Failure %r" % i)

    return render_template("index.html")


@obj.route('/about')
def about():
    return render_template("about.html")


@obj.route('/posts')
def posts():
    articles = Info.query.order_by(Info.date.desc()).all()
    return render_template("posts.html", articles=articles)


@obj.route('/posts/<int:id>')
def post_detail(id):
    article = Info.query.get(id)
    return render_template("post_detail.html", article=article)


@obj.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Info.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "Error"


@obj.route('/posts/<int:id>/update', methods=["POST", "GET"])
def post_update(id):
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        info = Info(title=title, intro=intro, text=text)

        try:
            db.session.add(info)
            db.session.commit()
            return redirect("/posts")
        except:
            return "Error"
    else:
        article = Info.query.get(id)
        return render_template("post_update.html", article=article)


@obj.route("/create--Info", methods=["POST", "GET"])
def create_Info():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        info = Info(title=title, intro=intro, text=text)

        try:
            db.session.add(info)
            db.session.commit()
            return redirect("/posts")
        except:
            return "Error"
    else:
        return render_template("create--Info.html")


if __name__ == "__main__":
    obj.run(debug=True)
