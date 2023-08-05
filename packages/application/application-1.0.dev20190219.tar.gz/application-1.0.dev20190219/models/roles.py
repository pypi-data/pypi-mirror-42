
from config import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
import os
import datetime
app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://bhanu:bhanu123@127.0.0.1/sam"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



class Roles(db.Model):
    __tablename__ = "roles"
    id         = db.Column(db.Integer, primary_key = True)
    name       = db.Column(db.String(50))
