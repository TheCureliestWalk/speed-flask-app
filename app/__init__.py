from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize

app = Flask(__name__)
db = SQLAlchemy(app)

# Config

app.config['DEBUG_MODE'] = True
app.config['SECRET_KEY'] = 'E09D9689D8511DA1D1575720FF7A2B99CC1494BA'
app.config['SQLALCHEMY_BINDS'] = {'local': 'sqlite:///database.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Routes

@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    if request.method == 'GET':
        data = {'message': 'App is running...'}
    else:
        data = {'message':'Not valid method.'}
    return jsonify(data)