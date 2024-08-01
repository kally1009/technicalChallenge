# database name is starwars.db with a galaxy_planet, star_wars_character and starship_master tables. 
# galaxy_planet table includes: id (int) PK, name (varchar), climate (varchar), population (int)
# star_wars_character table includes: id (int) PK, name(varchar), home_planet (int) FK, starships (blob) FK
# starship_master table includes: id (int) PK, name (varchar), model (varchar), cost_in_credits (int)

import sqlite3

# makes return easier to work with as a dictory instead of a tuple. 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# class to connect to database and methods with predefined queries to operate the database
class starwarsDB:
    # connecting to the actual database
    def __init__(self):
        self.connection= sqlite3.connect("starwars.db")
        self.connection.row_factory = dict_factory
        self.cursor= self.connection.cursor()
    
    def getAllPlanets(self):
        self.cursor.execute("SELECT * FROM galaxy_planet")
        items = self.cursor.fetchall()
        return items

    def getOnePlanet(self, planet_id):
        data = [planet_id]
        self.cursor.execute("SELECT * FROM galaxy_planet WHERE id = ?", data)
        planet = self.cursor.fetchone()
        return planet
        

    def createPlanet(self, name, climate, population):
        data= [name, climate, population]
        self.cursor.execute("INSERT INTO galaxy_planet (name, climate, population) VALUES (? , ?, ?)", data)
        self.connection.commit()
        

    def updatePlanet(self, planet_id, name, climate, population):
        data = [ name, climate, population, planet_id]
        self.cursor.execute("UPDATE galaxy_planet SET name = ?, climate = ?, population = ? WHERE id = ?", data)
        self.connection.commit()

    def deletePlanet(self, planet_id):
        data = [planet_id]
        self.cursor.execute("DELETE FROM galaxy_planet WHERE id = ?", data) 
        self.connection.commit()

    def getAllCharacters(self):
        self.cursor.execute("SELECT * FROM star_wars_character")
        items = self.cursor.fetchall()
        return items

    def getOneCharacter(self, character_id):
        data = [character_id]
        self.cursor.execute("SELECT * FROM star_wars_character WHERE id = ?", data)
        character = self.cursor.fetchone()
        return character
        

    def createCharacter(self, name, home_planet, starships):
        data= [name, home_planet, starships]
        self.cursor.execute("INSERT INTO star_wars_character (name, home_planet, starships) VALUES (? , ?, ?)", data)
        self.connection.commit()
        

    def updateCharacter(self, char_id, name, home_planet, starships):
        data = [ name, home_planet, starships, char_id]
        self.cursor.execute("UPDATE star_wars_character SET name = ?, home_planet = ?, starships = ? WHERE id = ?", data)
        self.connection.commit()

    def deleteCharacter(self, char_id):
        data = [char_id]
        self.cursor.execute("DELETE FROM star_wars_character WHERE id = ?", data) 
        self.connection.commit()

    def getAllStarships(self):
        self.cursor.execute("SELECT * FROM starship_master")
        items = self.cursor.fetchall()
        return items

    def getOneStarship(self, ship_id):
        data = [ship_id]
        self.cursor.execute("SELECT * FROM starship_master WHERE id = ?", data)
        character = self.cursor.fetchone()
        return character
        

    def createStarship(self, name, model, cost):
        data= [name, model, cost]
        self.cursor.execute("INSERT INTO starship_master (name, model, cost_in_credits) VALUES (? , ?, ?)", data)
        self.connection.commit()
        

    def updateStarship(self, ship_id, name, model, cost):
        data = [ name, model, cost, ship_id]
        self.cursor.execute("UPDATE starship_master SET name = ?, model = ?, cost_in_credits = ? WHERE id = ?", data)
        self.connection.commit()

    def deleteStarship(self, ship_id):
        data = [ship_id]
        self.cursor.execute("DELETE FROM starship_master WHERE id = ?", data) 
        self.connection.commit()
    
    # Create a native query that pulls the data for a character name, ship name, and planet name.
    def nativeQuery(self):
        self.cursor.execute("SELECT s.name as character_name, p.name as home_planet_name, s.starships FROM star_wars_character s JOIN galaxy_planet p ON p.ID = s.home_planet ORDER BY home_planet_name, character_name ASC")
        records = self.cursor.fetchall()
        return records