[![Build Status](https://travis-ci.org/Onyimatics/capstone.svg?branch=master)](https://travis-ci.org/Onyimatics/capstone)

# Capstone

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Required Features
### Models:
- Movies with attributes title and release date
- Actors with attributes name, age and gender

### Endpoints:
- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

## Roles:
### Casting Assistant
- Can view actors and movies

### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

### Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database

## Tests:
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

## Getting Started
### Clone this repo `https://github.com/Onyimatics/capstone.git`

- Navigate into the folder in your terminal

## Run the following command on your terminal
- `virtualenv venv`
- `pip install -r requirements.txt`
- `. setup.sh`
- `python manage.py db upgrade`
- `python manage.py seed`
- `flask run --reload`

## Access Details
### Click the login link below:
[Login to Auth0](https://onyinye-ezike.auth0.com/authorize?audience=video&response_type=token&client_id=PS3Qu2vcqEHx5ykd4Qfpy1JXFg23NINJ&redirect_uri=http://localhost:8080/login-results
) 
### and user the login details below to generate a token
#### The app uses a third-party service (Auth0) for authentication.

### The 3 login details are as follows:
 | Email | Password | Role |
 | ------ | --------|  ---- |
 | executive_producer@gmail.com|Executiveproducer@1|Executive Producer |
 | casting_director@gmail.com|Castingdirector@1|Casting Director|
 | casting_assistant@gmail.com|Castingassistant@1|Casting Assistant|

### NB: Grab the token from the address bar and use it on your postman Authorization by setting the Bearer Token.

## ENDPOINTS

### Use This [Heroku Base Url](https://onyinye-capstone.herokuapp.com) to access all the endpoints

 | Method | ROUTE | PERMISSION      | Role | Body | Description |
 | ------ | ----------- | -------------- | ---- |------------|-----|
 | Get | / | * | * | N/A | index page |
 | POST | /movies | post:movies | Executive Producer |{ title:"String", release_date:"YYYY-MM-DD" }| create a movie |
 | PATCH | /movies/id | patch:movies | Executive Producer/Casting Director |{ title:"String", release_date:"YYYY-MM-DD" }| Updates a movie |
 | GET | /movies | get:movies | All Registered Users  | N/A | Gets list of movies |
 | GET | /movies/id | get:movies | All Registered Users | N/A | Get a movie |
 | DELETE | /movies/id | delete:movies | Executive Producer | N/A | Delete a movie |
 | POST | /actors | post:actors | Executive Producer/Casting Director|{ name:"String", age:"Number", gender:"String" } |Create an actor |
 | PATCH | /actors/id | patch:actors | Executive Producer/Casting Director | { name:"optional String", age:"optional Number" gender:"optional String" }| Updates an actor |
 | GET | /actors | get:actors | All Registered Users | N/A | Gets list of actors |
 | GET | /actors/id | get:actors | All Registered Users | N/A | Get an actor |
 | DELETE | /actors/id | delete:actors | Executive Producer/Casting Director | N/A | delete an actor |


## Running test
- `python test_app.py`

## Technologies
- Python/Flask
- Auth0
- SQLAlchemy
- Flask-Migrate
- Flask-Script


## Authors
#### Onyinye Ezike - [Capstone](https://onyinye-capstone.herokuapp.com)