from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tatakae@localhost:5432/bank'
app.config['SECRET_KEY'] = 'MUITO_SEXO'

login_manager = LoginManager(app)
db = SQLAlchemy(app)

print(app.config['SQLALCHEMY_DATABASE_URI'])

