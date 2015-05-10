from flask import Flask

from blueprints.api import api
from models import db,User,Movie,Review #,Wishlist,Watchlist
import hashlib

app = Flask(__name__)
app.config.from_object('default_settings')
app.register_blueprint(api,url_prefix="/api")
db.init_app(app)

@app.route('/')
def hello_world():
  return "Hello World"

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
    #user = User(email_address="abcd@gmail.com", password_sha256=hashlib.sha256('1111').hexdigest(), name='abcd')
    #db.session.add(user)
    #movie = Movie(id=2661, name="Batman: The Dark Night")
    #db.session.add(movie)
    #userid=User.query.filter_by(name='abcd').first()
    #review = Review(userId=userid, movieId=2661, description="good", rating=4);
    #db.session.add(review)
    #wish = Wishlist(userId=userid,movieId=2661)
    #db.session.add(wish)
    #watch = Watchlist(userId=userid,movieId=2661)
    #db.session.add(watch)
    #print user.id, movie.id, review.id, movie.get()
    #db.session.commit()

  app.run(host="0.0.0.0",port=8000)
