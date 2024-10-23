import json
import logging
import sys
from flask import Flask, request, render_template, abort
from pymongo import MongoClient

import sites_of_grace

app = Flask(__name__)

######## MongoDB stuff
client = MongoClient("localhost", 27017) #create an instance of MongoDB named client
db = client.flask_db #read (or create when it doesn't exist) a database within the client instance called flask_db
locations = db.locations #read (or create when it doesn't exist) a collection called locations. Collection stores data called documents
########

#set up logging
logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(403)
def forbidden_error(error):
    app.logger.error("403 error occurred: %s", error)
    return "403 Forbidden", 403

@app.route("/", methods=['GET'])
def createForm():
    allLocs = locations.find() #returns all documents in locations
    sites_of_grace.createMap(allLocs)
    return render_template("map.html", source = sites_of_grace.map.sitesOfGracesFullName, destination = sites_of_grace.map.sitesOfGracesFullName) 
    #when this form is submitted, send the data in the form to whatever URL is generated by url_for('getPath')

@app.route("/getpath", methods=["GET"])
def getPath():
    try:
        # print("REQUEST --------------", request)
        # print("REQUEST ARGS --------------", request.args)
        destinationID = request.args.get("destination", "")
        destinationIDUpper = destinationID.upper()
        sourceID = request.args.get("source", "")
        sourceIDUpper = sourceID.upper()
        #path = sites_of_grace.findPath("Gravesite Plain", "Three-Path Cross")
        #print("----------------", destinationIDUpper, "     ", sourceIDUpper)
        pathDict = sites_of_grace.findPath(sourceIDUpper, destinationIDUpper)
        return render_template("results.html", source = sites_of_grace.map.sitesOfGracesFullName, destination = sites_of_grace.map.sitesOfGracesFullName, path = pathDict["pathName"])
    except Exception as e:
        app.logger.error("Error in getPath: %s", str(e))
        abort(403)

if __name__ == "__main__":
   app.run()
