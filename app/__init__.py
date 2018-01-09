from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

from app.bill.controllers import mod_bill

app.register_blueprint(mod_bill)
