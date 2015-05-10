import movieService
import simplejson as json
from flask import Blueprint, request, jsonify, Response
from models import db, User, Review, Movie
from bson.json_util import dumps

api = Blueprint('api',__name__)

#API routes

@api.route('/movies/search/<searchKey>')
def searchMovies(searchKey):
  a = (movieService.findMovieByKeyword(searchKey))
  responseJson = map(dictToJson, a)
  return Response(dumps(responseJson), mimetype='application/json')

@api.route('/movie/<int:id>')
def getMovieById(id):
  movieData = movieService.findMovieById(id)
  responseJson = dictToJson(movieData[0])
  return Response(dumps(responseJson), mimetype='application/json')

@api.route('/user/<userMail>', methods = ["GET"])
def getUserById(userMail):
  user = User.query.filter_by(email_address=userMail).first()
  print user.__dict__
  userStorage = user.__dict__
  result = {}
  result['email_address'] = userStorage['email_address']
  result['name'] =userStorage['name']
  result['id'] = userStorage['id']
  return Response(dumps(result), mimetype='application/json')

# /api/user/1/movie/268/review
@api.route('/user/<int:userId>/movie/<int:movieId>/review', methods=["POST"])
def addReview(userId, movieId):
  postData = request.data
  postBody = json.loads(postData)
  review = Review( userId =userId, movieId =movieId, description = postBody["description"], rating = postBody["rating"])
  db.session.add(review)
  db.session.commit()
  postBody["userId"]=userId
  postBody["movieId"]=movieId
  return Response(dumps(postBody), mimetype='application/json')

@api.route('/user/<int:userId>/watchList/<int:movieId>', methods=["POST"])
def addToWatchList(userId, movieId):
  postData = request.data
  postBody = json.loads(postData)
  watchList = WatchList(userId, movieId)
  db.session.add(watchList)
  db.session.commit()
  return Response(dumps(postData), mimetype='application/json')

@api.route('/user/<int:userId>/wishList/<int:movieId>', methods=["POST"])
def addToWishList(userId, movieId):
  postData = request.data
  postBody = json.loads(postData)
  wishList = WishList(userId, movieId)
  db.session.add(wishList)
  db.session.commit()
  return Response(dumps(postData), mimetype='application/json')

@api.route('/user/<int:userId>/reviews', methods = ["GET"])
def getReviewsByUserId(userId):
  review = Review.query.filter_by(userId=userId)
  review = [r for r in review]
  reviewResult = map(reviewToResult,review)
  return Response(dumps(reviewResult), mimetype='application/json')

@api.route('/movie/<int:movieId>/reviews', methods = ["GET"])
def getReviewsByMovieId(movieId):
  review = Review.query.filter_by(movieId=movieId)
  review = [r for r in review]
  reviewResult = map(reviewToResult,review)
  return Response(dumps(reviewResult), mimetype='application/json')

def dictToJson(movieDict):
  data = movieDict['_data']
  finalDict = data
  finalDict['poster_path'] = "http://image.tmdb.org/t/p/w500/"+data['poster_path']['_data']['file_path']
  return finalDict

def reviewToResult(review):
  reviewDict = review.__dict__
  reviewResult = {}
  reviewResult['userId'] = reviewDict['userId']
  reviewResult['movieId'] = reviewDict['movieId']
  reviewResult['description'] = reviewDict['description']
  reviewResult['rating'] = reviewDict['rating']
  return reviewResult
