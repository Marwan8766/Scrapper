from flask import Flask, request, jsonify
from utils.googleMapsScrapper import find_places_in_city
from utils.scrappingLink import fill_place_details
from utils.placeClass import Place
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from config.env
load_dotenv("config.env")


@app.route('/api/v1/places', methods=['GET'])
def get_places():
    """
    returns array of places objects with name , link , rating

    :param query: The query which will be searched with in the search box of googlemaps. (required)
    :type query: string
    :param placesLength: The length of the places array. (not required)
    :type placesLength: int

    """ 
    try:
      # get the query and placesLength from the url
      query = request.args.get('query').lower().strip()

      placesLength = request.args.get('placesLength')
      if placesLength is not None and placesLength.isnumeric():
       placesLength = int(placesLength)
      else:
        placesLength = None

      
      places = find_places_in_city(query)


      if placesLength is not None:  
          places = find_places_in_city(query,placesLength)

      places_list = [place.to_dict() for place in places]

      return jsonify({
        'status':"success",
        'data': places_list,
        'dataLength': len(places_list)
      }),200
    except Exception as e:
      print(e)
      return jsonify({
        'status':"fail",
        'message': "Error finding the places"
      }),404
    

@app.route('/api/v1/places/fullDetails', methods=['GET'])
def get_places_full_details():
    """
    returns array of places objects with name , link , rating , description , type , image , open close times 

    :param query: The query which will be searched with in the search box of googlemaps. (required)
    :type query: string
    :param placesLength: The length of the places array. (not required)
    :type placesLength: int

    """ 
    try:
      # get the query and placesLength from the url
      query = request.args.get('query').lower().strip()

      placesLength = request.args.get('placesLength')
      if placesLength is not None and placesLength.isnumeric():
       placesLength = int(placesLength)
      else:
        placesLength = None

      
      places = find_places_in_city(query)


      if placesLength is not None:  
          places = find_places_in_city(query,placesLength)
      
      placesFullDetails = []

      for place in places:
         fill_place_details(place)
         placesFullDetails.append(place)
      
      places_list = [place.to_dict() for place in placesFullDetails]


      return jsonify({
        'status':"success",
        'data': places_list,
        'dataLength': len(places_list)
      }),200
    
    except Exception as e:
      print(e)
      return jsonify({
        'status':"fail",
        'message': "Error finding the places"
      }),404



@app.route('/api/v1/places/place', methods=['GET'])
def get_place():
    """
    returns place object with name , link , rating , description , type , image , open close times

    :param place: The place object to be modified. (required)
    :type place: dictionary (object)

    """ 
    try:
      # retrieve the place name from the request body
      name = request.json.get('name')
        
      # retrieve the place rating from the request body
      rating = request.json.get('rating')
        
      # retrieve the place link from the request body
      link = request.json.get('link')
        
      # create new place
      updatedPlace = Place()

      # add the fields of place to updated place
      updatedPlace.name = name
      updatedPlace.link = link
      if rating:
          updatedPlace.rating = rating

      # add the full details to the updatedPlace
      fill_place_details(updatedPlace)

      # change the updatedPlace to dictionary
      updatedPlace = updatedPlace.to_dict()

      return jsonify({
        'status':"success",
        'data': updatedPlace,
      }),200
    
    except Exception as e:
      print(e)
      return jsonify({
        'status':"fail",
        'message': "Error finding the places"
      }),404
    


# Access environment variables
port = os.getenv("PORT")

if __name__ == '__main__':
    app.run(port=port | 3000)
