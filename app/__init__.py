from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app.bill.controllers import mod_bill

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object("config")

app.register_blueprint(mod_bill)

