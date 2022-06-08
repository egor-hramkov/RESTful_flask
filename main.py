import os
from datetime import datetime
import requests
from flask import Flask, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import json

from flask_session import Session
from flask_login import LoginManager

DATABASE = 'flsite.db'
DEBUG = True
SECRET_KEY = '&8\xa2|\x11\x0f\xcf\xe8\xc2\xa6\x85"\xfd~\x0c#\x06{>T\xb7\xe9\xd8\xc9'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
app.config['SESSION_PEMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///maindb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
Session(app)
db = SQLAlchemy(app)
api = Api()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(50), nullable = False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique = False)
    age = db.Column(db.Integer, nullable = False)
    password = db.Column(db.String(500), nullable = False)
    role = db.Column(db.String(50), nullable=False)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maintext = db.Column(db.String(5000), nullable=False)
    category = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, ForeignKey("users.id", ondelete='CASCADE'))

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100), nullable=True)

class Main(Resource):
    all_news = News.query.all()

    def get(self, news_id, all_news = all_news):
        dict_news = {
        }
        for i in range(len(all_news)):
            dict_news[i] = {
                "id": all_news[i].id,
                "text": all_news[i].maintext,
                "date_created": all_news[i].date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "author": Users.query.filter_by(id = all_news[i].user_id).first().name + " " + Users.query.filter_by(id = all_news[i].user_id).first().surname
                }
        return json.dumps(dict_news[news_id - 1], ensure_ascii=False)


api.add_resource(Main, "/news/<int:news_id>")
api.init_app(app)

@app.route('/')
@app.route('/mainpage/')
def mainpage():
    return render_template('mainpage.html')




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')