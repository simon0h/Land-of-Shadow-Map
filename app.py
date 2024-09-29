import json
import logging
from flask import Flask, request, render_template, abort
from pymongo import MongoClient

import sites_of_grace

app = Flask(__name__)

client = MongoClient("localhost", 27017) #create a client instance of MongoDB
db = client.flask_db #create/read a database within the client instance called flask_db
locations = db.locations #create/read a collection called locations

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(403)
def forbidden_error(error):
    app.logger.error("403 error occurred: %s", error)
    return "403 Forbidden", 403

@app.route("/", methods=['GET'])
def createForm():
    return render_template("form.html")

@app.route("/getpath", methods=["GET"])
def getPath():
    try:
        allLocs = locations.find()
        sites_of_grace.createMap(allLocs)
        destinationID = request.args.get("destination", "")
        destinationIDUpper = destinationID.upper()
        sourceID = request.args.get("source", "")
        sourceIDUpper = sourceID.upper()
        #path = sites_of_grace.findPath("Gravesite Plain", "Three-Path Cross")
        #print(destinationIDUpper, sourceIDUpper)
        path = sites_of_grace.findPath(sourceIDUpper, destinationIDUpper)
        return render_template("results.html", path = path)
    except Exception as e:
        app.logger.error("Error in getPath: %s", str(e))
        abort(403)

if __name__ == "__main__":
   app.run()
