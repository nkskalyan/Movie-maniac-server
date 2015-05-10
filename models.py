from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ =  'user'
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(80), unique=True)
    password_sha256 = db.Column(db.String(64))
    dp = db.Column(db.String(80))
    name = db.Column(db.String(80))
    reviews = db.relationship('Review', backref='review', lazy='dynamic')
    wishlist = db.relationship('Wishlist', backref='wishlist', lazy='dynamic')
    watchlist = db.relationship('Watchlist', backref='watchlist', lazy='dynamic')

    def __init__(self, email_address, password_sha256, name='', dp=''):
        self.email_address = email_address
        self.password_sha256 = password_sha256
        self.name = name
        self.dp = dp

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email_address

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    movieId = db.Column(db.Integer, db.ForeignKey('movie.id'))
    description = db.Column(db.String(80))
    rating = db.Column(db.Integer)

    def __init__(self, userId, movieId, description, rating):
      self.userId = userId
      self.movieId = movieId
      self.description = description
      self.rating = rating

class Movie(db.Model):
  __tablename__ = 'movie'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))

  def __init__(self, id, name):
    self.id = id
    self.name = name

class Wishlist(db.Model):
  __tablename__ = 'wishlist'
  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('user.id'))
  movieId = db.Column(db.Integer, db.ForeignKey('movie.id'))

  def __init__(self, userId, movieId):
    self.userId = userId
    self.movieId = movieId

class Watchlist(db.Model):
  __tablename__ = 'watchlist'
  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('user.id'))
  movieId = db.Column(db.Integer, db.ForeignKey('movie.id'))
  watchCount = db.Column(db.Integer)
  def __init__(self, userId, movieId, watchCount=1):
    self.userId = userId;
    self.movieId = movieId;
