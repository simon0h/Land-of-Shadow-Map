# import json
# from flask import Flask, request

# import sites_of_grace

# app = Flask(__name__)

# # @app.route("/", methods=['GET'])
# # def getPath():
# #     sites_of_grace.createMap("sites.json")
# #     path = sites_of_grace.findPath("GP-GP", "B-TDB")
# #     return path

# # @app.route("/", methods=['POST'])
# # def postPath():
# #     return "post"

# if __name__ == '__main__':
#    app.run()

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    print("hello")  # This explains the "hello" in the logs
    app.run()
