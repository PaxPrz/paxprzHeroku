from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
import datetime

db = SQLAlchemy()

class Login(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    ip = db.Column(db.String(40))
    agent = db.Column(db.String(100))
    timeStamp = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, ip, agent, timestamp):
        self.username = username if len(username)<20 else username[:20]
        self.ip = ip if len(ip)<40 else ip[:40]
        self.agent = agent if len(agent)<100 else agent[:100]
        self.timeStamp = timestamp

class GitHub(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    # ip = db.Column(db.String(50))
    timeStamp = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, timestamp):
        self.username = username if len(username)<20 else username[:20]
        # self.ip = ip if len(ip)<40 else ip[:40]
        self.timesStamp = timestamp

class StackOverFlow(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    # ip = db.Column(db.String(50))
    timeStamp = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, timestamp):
        self.username = username if len(username)<20 else username[:20]
        # self.ip = ip if len(ip)<40 else ip[:40]
        self.timeStamp = timestamp

class LinkedIn(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    # ip = db.Column(db.String(50))
    timeStamp = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, timestamp):
        self.username = username if len(username)<20 else username[:20]
        # self.ip = ip if len(ip)<40 else ip[:40]
        self.timeStamp = timestamp

class CV(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(40))
    name = db.Column(db.String(40))
    contact = db.Column(db.String(20))
    ip = db.Column(db.String(50))
    timeStamp = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, email, name, contact, ip, timestamp):
        self.username = username if len(username)<20 else username[:20]
        self.email = email if len(email)<40 else email[:40]
        self.name = name if len(name)<40 else name[:40]
        self.contact = contact if len(contact)<20 else contact[:20]
        self.ip = ip if len(ip)<40 else ip[:40]
        self.timeStamp = timestamp

def create_tables():
    db.create_all()
    db.session.commit()
    print(' --- created database --- ')