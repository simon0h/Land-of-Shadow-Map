import json

class SitesOfGrace:
    def __init__(self, name, region, id, isDungeon):
        self.name = name
        self.region = region
        self.id = id
        self.isDungeon = isDungeon
        self.neighborsID = []
        self.neighborsObj = []
        self.visited = False

    def findPath(self, pathID, pathName, id) -> bool:
        #DFS, not shortest
        #rewrite
        if (self.id == id):
            pathID.append(self.id)
            pathName.append(self.name)
            return True
        if (self.visited):
            return False
        self.visited = True
        for neighbor in self.neighborsObj:
            if neighbor.findPath(pathID, pathName, id):
                self.visited = False
                pathID.append(self.id)
                pathName.append(self.name)
                return True
        self.visited = False
        return False

class Map:
    sitesOfGraces = {}
    sitesOfGracesFullName = {}

map = Map()

def createMap(sitesDoc):
    for indvSite in sitesDoc:
        site = SitesOfGrace(indvSite["name"], indvSite["region"], indvSite["id"], indvSite["isDungeon"])
        for neighbor in indvSite["neighbors"]:
            site.neighborsID.append(neighbor["id"])
        map.sitesOfGraces[indvSite["id"]] = site
        map.sitesOfGracesFullName[indvSite["name"]] = indvSite["id"]
        #print(indvSite["name"], indvSite["id"])

    for i in map.sitesOfGraces:
        for neighborID in map.sitesOfGraces[i].neighborsID:
            obj = map.sitesOfGraces[neighborID]
            map.sitesOfGraces[i].neighborsObj.append(obj)

def findPath(source, destination):
    #print(source, destination)
    sourceIDName = getID(source)
    destinationIDName = getID(destination)
    if (sourceIDName == "none" and destinationIDName == "none"):
        return "Source and destination not found"
    if (sourceIDName == "none"):
        return "Source not found"
    if (destinationIDName == "none"):
        return "Destination not found"
    obj = map.sitesOfGraces[sourceIDName]
    pathID = []
    pathName = []
    obj.findPath(pathID, pathName, destinationIDName)
    pathDetails = {"source": sourceIDName, "destination": destinationIDName, "pathExists": False, "pathID": pathID, "pathName": pathName}
    if (len(pathID) > 0):
        pathDetails["pathExists"] = True
    jsonPath = json.dumps(pathDetails)
    return jsonPath

def getID(fullName):
    return map.sitesOfGracesFullName.get(fullName, "none")

def getNames(ID):
    return map.sitesOfGraces.get(ID)
