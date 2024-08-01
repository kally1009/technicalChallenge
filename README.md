
# Starwars API - Kalicia Ashcraft

### galaxy_planet

Attributes:

* name (varchar)
* climate (varchar)
* population (varchar)

### star_wars_character

Attributes:

* name (varchar)
* home_planet (int)
* starships (blob)

### starship_master

Attributes:

* name (varchar)
* model (varchar)
* cost_in_credits (int)


Schema
---
```sql
CREATE TABLE galaxy_planet(ID INTEGER PRIMARY KEY,
name VARCHAR,
climate VARCHAR,
population INT);

CREATE TABLE star_wars_character(ID INTEGER PRIMARY KEY,
name VARCHAR,
home_planet INT REFERENCES galaxy_planet,
starships BLOB REFERENCES starship_master);

CREATE TABLE starship_master(ID INTEGER PRIMARY KEY,
name VARCHAR,
model VARCHAR,
cost_in_credits INT);
````

### CRUD Endpoints - Create, Retrieve, Update, Delete

#### planet endpoints
---
Name | Method | Path
------------ | ------------- | --------
Retrieve planets | GET | /planets
Retrieve specific planet | GET | /planets/id
Create planet | POST | /planets
Update specific planet | PUT | /planets/id
Delete specific planet | DELETE | /planets/id

#### character endpoints
---
Name | Method | Path
------------ | ------------- | --------
Retrieve starwars_characters | GET | /characters
Retrieve specific starwars_character | GET | /characters/id
Create starwars_character| POST | /characters
Update specific starwars_character | PUT | /characters/id
Delete specific starwars_character | DELETE | /characters/id

#### starship endpoints
---
Name | Method | Path
------------ | ------------- | --------
Retrieve starships | GET | /starships
Retrieve specific starship | GET | /starships/id
Create starship | POST | /starships
Update specific starship | PUT | /starship/id
Delete specific starship | DELETE | /starships/id

#### Native Query - Pulls the data for a character name, ship name, and planet name
---
Name | Method | Path
------------ | ------------- | --------
Retrieve native query | GET | /native-query




