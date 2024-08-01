from socketserver import ThreadingMixIn 
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from starwars_db import starwarsDB

class MyRequestHandler(BaseHTTPRequestHandler): 

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    # function to handle 404 - Not Found
    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not Found.", "utf-8"))
    
    # function to handle 400 - Bad Request
    def handleBadRequest(self):
        self.send_response(400)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Bad Request. Don't give into the dark side...", "utf-8"))

    # function to list all planets
    def handleListPlanets(self):
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        db=starwarsDB() # connect to database
        allRecords=db.getAllPlanets() # database operation
        self.wfile.write(bytes(json.dumps(allRecords),"utf-8")) #returns a json list to the user
            
    # function to get one planet
    def handleRetrievePlanet(self, planet_id):    
        db = starwarsDB() #connect to database
        planetRecord = db.getOnePlanet(planet_id) #grab one planet with the planet_id
        if planetRecord !=None: #if it exists then return the planet record
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(planetRecord), "utf-8"))
        else:
            self.handleNotFound()

    # function to update a planet
    def handleUpdatePlanet(self,planet_id):
        length = int (self.headers["Content-Length"])
        request_body=json.loads(self.rfile.read(length)) #read and load json object
        print("the request body:", request_body) 
        
        db=starwarsDB() #database connection
        PlanetRecord=db.getOnePlanet(planet_id) #get the requested record
        if PlanetRecord!=None: #if it exists, update the record
            try:
                name = request_body['name']
                climate = request_body['climate']
                population = request_body['population']
                print("Planet Updated info: ", name, climate,population)
                print("Updating")
                db.updatePlanet(planet_id, name, climate, population)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes("Updated.", "utf-8"))
            except:
                self.handleBadRequest()
        else:
            self.handleNotFound()
    
    # function to delete planet
    def handleDeletePlanet(self,planet_id):
        db = starwarsDB() #database connection
        planetRecord = db.getOnePlanet(planet_id) #get the requested record
        if planetRecord !=None: # if it exists, delete that record
            db.deletePlanet(planet_id)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Deleted.", "utf-8"))
        else:
            self.handleNotFound()

    # function to create planet
    def handleCreatePlanet(self):
        length = int (self.headers["Content-Length"])
        request_body=json.loads(self.rfile.read(length)) #reads and loads json object with data to create planet
        print("the request body:", request_body) 

        try:
            name = request_body['name']
            climate = request_body['climate']
            population = request_body['population']
            print("New Planet info: ", name, climate, population)
            db = starwarsDB() #database connection
            db.createPlanet(name, climate, population) #create planet
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("Created.", "utf-8"))
        except:
            self.handleBadRequest()

    def handleListCharacters(self):
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            db=starwarsDB()
            allRecords=db.getAllCharacters()
            self.wfile.write(bytes(json.dumps(allRecords),"utf-8"))
            
    
    def handleRetrieveCharacter(self, char_id):    
        db = starwarsDB()
        charRecord = db.getOneCharacter(char_id)
        if charRecord !=None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(charRecord), "utf-8"))
        else:
            self.handleNotFound()

    def handleUpdateCharacter(self,char_id):
        length = int (self.headers["Content-Length"])
        request_body=json.loads(self.rfile.read(length))
        print("the request body:", request_body) 
        db=starwarsDB()
        charRecord=db.getOneCharacter(char_id)
        if charRecord!=None:
            try:
                name = request_body['name']
                galaxy_planet = request_body['home_planet']
                starships = request_body['starships']
                print("Updating")
                db.updateCharacter(char_id, name, galaxy_planet, starships)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes("Updated.", "utf-8"))
            except:
                self.handleBadRequest()
        else:
            self.handleNotFound()
    
    def handleDeleteCharacter(self,char_id):
        db = starwarsDB()
        charRecord = db.getOneCharacter(char_id)

        if charRecord !=None:
            db.deleteCharacter(char_id)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Deleted.", "utf-8"))
        else:
            self.handleNotFound()


    def handleCreateCharacter(self):
        length = int (self.headers["Content-Length"])
        request_body=json.loads(self.rfile.read(length))
        print("the request body:", request_body) 

        try:
            name = request_body['name']
            home_planet = request_body['home_planet']
            starships = request_body['starships']
            print("New Character Info: ", name, home_planet, starships)
            db = starwarsDB()
            db.createCharacter(name, home_planet, starships)  
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("Created.", "utf-8"))
        except:
            self.handleBadRequest()
    
    def handleListStarships(self):
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            db=starwarsDB()
            allRecords=db.getAllStarships()
            self.wfile.write(bytes(json.dumps(allRecords),"utf-8"))
            
    
    def handleRetrieveStarship(self, ship_id):    
        db = starwarsDB()
        shipRecord = db.getOneStarship(ship_id)
        if shipRecord !=None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(shipRecord), "utf-8"))
        else:
            self.handleNotFound()

    def handleUpdateStarship(self,ship_id):
        length = int (self.headers["Content-Length"])
        request_body=json.loads(self.rfile.read(length))
        print("the request body:", request_body) 

        db=starwarsDB()
        shipRecord=db.getOneStarship(ship_id)
        if shipRecord!=None:
            try:
                name = request_body['name']
                model = request_body['model']
                cost = request_body['cost_in_credits']
                print("Updating")
                db.updateStarship(ship_id, name, model, cost)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes("Updated.", "utf-8"))
            except:
                self.handleBadRequest()
        else:
            self.handleNotFound()
    
    def handleDeleteStarship(self,ship_id):
        db = starwarsDB()
        shipRecord = db.getOneStarship(ship_id)

        if shipRecord !=None:
            db.deleteStarship(ship_id)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Deleted.", "utf-8"))
        else:
            self.handleNotFound()


    def handleCreateStarship(self):
        length = int (self.headers["Content-Length"])
        request_body=json.loads(self.rfile.read(length))
        print("the request body:", request_body) 

        try:
            name = request_body['name']
            model = request_body['model']
            cost = request_body['cost_in_credits']
            print("New starship info: ", name, model, cost)
            db = starwarsDB()
            db.createStarship(name, model, cost)  
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("Created.", "utf-8"))
        except:
            self.handleBadRequest()

    # Handling native query 
    def handleNativeQuery(self):
        db = starwarsDB()
        records = db.nativeQuery()
        print("the records are ", records)
        if records !=None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(records), "utf-8"))
        else:
            self.handleNotFound()

    #Preflight request for cors
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
    
    # Read(GET) Route Handler
    def do_GET(self):
        print("The request path is", self.path)
        path_parts = self.path.split('/')
        collection = path_parts[1]
        if len(path_parts) > 2:
            item_id = path_parts[2]
        else: 
            item_id = None
        if collection == "planets":
            if item_id:
                self.handleRetrievePlanet(item_id)
            else:
                self.handleListPlanets()
        elif collection=="characters":
            if item_id:
                self.handleRetrieveCharacter(item_id)
            else:
                self.handleListCharacters()
        elif collection=="starships":
            if item_id:
                self.handleRetrieveStarship(item_id)
            else:
                self.handleListStarships()
        elif collection=="native-query":
            self.handleNativeQuery()
        else:
            self.handleNotFound()

    # Create(POST) Route Handler
    def do_POST(self):
        print("The request path is", self.path)
        if self.path == "/planets":
            self.handleCreatePlanet()
        elif self.path=="/characters":
            self.handleCreateCharacter()
        elif self.path == "/starships":
            self.handleCreateStarship()
        else:
            self.handleNotFound()

    #Delete Route Handler
    def do_DELETE(self):
        print("The request path is", self.path)
        path_parts = self.path.split('/')
        collection = path_parts[1]
        if len(path_parts) > 2:
            item_id = path_parts[2]
        else: 
            item_id = None

        if collection == "planets":
            if item_id:
                self.handleDeletePlanet(item_id)
            else:
                self.handleNotFound()
        elif collection == "characters":
            if item_id:
                self.handleDeleteCharacter(item_id)
            else:
                self.handleNotFound()
        elif collection == "starships":
            if item_id:
                self.handleDeleteStarship(item_id)
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()

    # UPDATE(PUT) Route Handler
    def do_PUT(self):
        print("The request path is", self.path)
        path_parts = self.path.split('/')
        collection = path_parts[1]
        if len(path_parts) > 2:
            item_id = path_parts[2]
        else: 
            item_id = None

        if collection =="planets":
            if item_id:
                self.handleUpdatePlanet(item_id)
            else:
                self.handleNotFound()
        elif collection == "characters":
            if item_id:
                self.handleUpdateCharacter(item_id)
            else:
                self.handleNotFound()
        elif collection == "starships":
            if item_id:
                self.handleUpdateStarship(item_id)
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()

# Uses threads to handle requests
class ThreadedHTTPServer(ThreadingMixIn,HTTPServer):
    pass #nothing to see here ;) 

# Main server function
def run():
    listen=("127.0.0.1", 5000)
    server = ThreadedHTTPServer(listen,MyRequestHandler)
    print("The Server is Running!")
    server.serve_forever()
    print("This will never, ever execute.")

run()

# python3 server.py
# To start the server. 