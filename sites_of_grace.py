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

    def findPath(self, path, id) -> bool:
        #DFS, not shortest
        #rewrite
        if (self.id == id):
            path.append(self.id)
            return True
        if (self.visited):
            return False
        self.visited = True
        for neighbor in self.neighborsObj:
            if neighbor.findPath(path, id):
                self.visited = False
                path.append(self.id)
                return True
        self.visited = False
        return False

class Map:
    sitesOfGraces = {}

map = Map()

def createMap(sitesPath):
    f = open(sitesPath)
    data = json.load(f)
    for indvSite in data:
        site = SitesOfGrace(indvSite["name"], indvSite["region"], indvSite["id"], indvSite["isDungeon"])
        for neighbor in indvSite["neighbors"]:
            site.neighborsID.append(neighbor["id"])
        map.sitesOfGraces[indvSite["id"]] = site
    f.close()

    for i in map.sitesOfGraces:
        for neighborID in map.sitesOfGraces[i].neighborsID:
            obj = map.sitesOfGraces[neighborID]
            map.sitesOfGraces[i].neighborsObj.append(obj)

def findPath(source, destination):
    obj = map.sitesOfGraces[source]
    path = []
    obj.findPath(path, destination)
    pathDetails = {"source": source, "destination": destination, "pathExists": False, "path": path}
    if (len(path) > 0):
        pathDetails["pathExists"] = True
    jsonPath = json.dumps(pathDetails)
    return jsonPath
