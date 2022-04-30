from flask import Flask

from jinja2.utils import markupsafe 
markupsafe.Markup()


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'