import re
import tmdb3
import pymongo
import datetime
from urllib2 import Request, urlopen, URLError

api_key='7fb362b555787b7add015e35fcadad84'
tmdb3.set_key(api_key)
client = pymongo.MongoClient('localhost', 27017)
db = client['MoviesDB']
movies = db['Movies']

def findMovieById(mId):
  try:
    searchResults = movies.find({"_data.id": mId})
    #Return searchResults.toList or something equivalent
    return list(searchResults)
    ##for movie in searchResults:
    ##  print movie
    """
    request = Request('https://api.themoviedb.org/3/movie/'+mId+'?api_key='+api_key)
    movies.insert_one(); ///to be continued"""
  except pymongo.errors.PyMongoError as e:
    print "ERROR: ",e

def findMovieByKeyword(keyword):
  try:
    #Use search array
    keyword = keyword.lower()
    regx = re.compile(keyword, re.IGNORECASE)

    searchResults = movies.find({'search_key': {'$regex':keyword}}) #{$regex:/keyword/i}})
    #print list(searchResults)
    result = list(searchResults)
    if len(result) == 0:
      insertIntoDB(keyword)
      searchResults = movies.find({'search_key': {'$regex':keyword}}) #{$regex:/keyword/i}})
      result = list(searchResults)
    return result
  except pymongo.errors.PyMongoError as e:
    print "ERROR: ",e

def insertIntoDB(keyword):
  keyword = keyword.lower()
  try:
    searchResults = tmdb3.searchMovie(keyword)
    for searchItem in searchResults:
      jsonMovieData = toRecursiveDict(searchItem.__dict__)
      jsonMovieData['search_key'] = keyword
      movies.insert_one(jsonMovieData)
  except pymongo.errors.PyMongoError as e:
    print "ERROR: ",e

def toRecursiveDict(obj):
        a = {}
        for key in obj.keys():
                if key == '_locale':
                        continue
                elif isinstance(obj[key], datetime.date):
                        a[key] = str(obj[key])
                elif not isinstance(obj[key], int) and  not isinstance(obj[key], str) :
                        if not isinstance(obj[key],dict) and hasattr(obj[key],"__dict__"):
                                a[key]=obj[key].__dict__
                                a[key]=toRecursiveDict(a[key]);
                        elif isinstance(obj[key],dict):
                                a[key]=toRecursiveDict(obj[key])
                        else:
                                a[key] = obj[key]
                else:
                        a[key] = obj[key]
        return a

if __name__=='__main__':
##  insertIntoDB("lord of the rings")
  print findMovieById(155)
