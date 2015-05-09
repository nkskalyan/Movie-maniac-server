import movieService
import simplejson as json
from flask import Blueprint, request, jsonify, Response

from bson.json_util import dumps

api = Blueprint('api',__name__)

#API routes

@api.route('/movies/search/<searchKey>')
def searchMovies(searchKey):
  a = (movieService.findMovieByKeyword(searchKey))
  #print dumps(a)
  #return dumps(a)
  return Response(dumps(a), mimetype='application/json')

@api.route('/movie/<int:id>')
def getMovieById(id):
  responseJson = movieService.findMovieById(id)
  return Response(dumps(responseJson[0]), mimetype='application/json')
