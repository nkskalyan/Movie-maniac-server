from flask import Flask

from blueprints.api import api

app = Flask(__name__)
app.register_blueprint(api,url_prefix="/api")

@app.route('/')
def hello_world():
  return "Hello World"

if __name__ == '__main__':
  app.debug = True
  app.run(host="0.0.0.0",port=8000)