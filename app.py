from flask import Flask

from blueprints.api import api
from models import db

app = Flask(__name__)
app.config.from_object('default_settings')
app.register_blueprint(api,url_prefix="/api")

@app.route('/')
def hello_world():
  return "Hello World"

if __name__ == '__main__':
  db.init_app(app)
  app.run(host="0.0.0.0",port=8000)
