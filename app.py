import json

from flask import Flask, render_template,url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from norm import *
import pickle
module= pickle.load(open('pipe.pkl','rb'))

app=Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FakeNews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/posts')
def posts():
    articles=Article.query.order_by(Article.date).all()
    return render_template ("posts.html",articles=articles)

@app.route('/create-article',methods=['POST','GET'])
def create_article():
    if request.method == "POST":
        text = request.form['text']
        prediction=module.predict([text])
        return redirect(url_for('create_article',data={'text':text,'pred':prediction[0]}))
    else:
        return render_template('create-article.html',data={'text':"",'pred':""})



if __name__=="__main__":
    app.run(debug=True)





