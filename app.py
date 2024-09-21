import json
import logging
from flask import Flask, request, render_template, abort

import sites_of_grace

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(403)
def forbidden_error(error):
    app.logger.error('403 error occurred: %s', error)
    return "403 Forbidden", 403

@app.route("/", methods=['GET'])
def createForm():
    return render_template('form.html')

@app.route("/", methods=['POST'])
def getPath():
    try:
        sites_of_grace.createMap("sites.json")
        destinationID = request.form["destination"]
        destinationIDUpper = destinationID.upper()
        sourceID = request.form["source"]
        sourceIDUpper = sourceID.upper()
        path = sites_of_grace.findPath("Gravesite Plain", "Three-Path Cross")
        #path = sites_of_grace.findPath(destinationIDUpper, sourceIDUpper)
        return path
    except Exception as e:
        app.logger.error('Error in getPath: %s', str(e))
        abort(403)

if __name__ == '__main__':
   app.run(debug=True)
