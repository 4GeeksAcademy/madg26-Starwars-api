"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Character, Planet, Starship
#from models import Person



app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def all_users():
    users = User.query.all()
    all_user = list(map(lambda user: user.serialize(), users))
    return (
        jsonify({"data": all_user})
    )
@app.route('/user', methods=['POST'])
def new_user():
     body = request.get_json(silent = True)
     if body is None:
          return ({'msg' : 'Debes enviar informacion'}), 400
     if 'email' not in body:
          return jsonify({'msg' : 'El campo email es obligatorio'})
     if 'username' not in body:
          return jsonify({'msg' : 'El campo username es obligatorio'})
     if 'firstname' not in body:
          return jsonify({'msg' : 'El campo firstname es obligatorio'})
     if 'lastname' not in body:
          return jsonify({'msg' : 'El campo lastname es obligatorio'})
     if 'password' not in body:
          return jsonify({'msg'  : 'El campo password en obligatorio'})
     
     new_user = User()
     new_user.email = body['email']
     new_user.username = body['username']
     new_user.firstname = body['firstname']
     new_user.lastname = body['lastname']
     new_user.password = body['password']

     db.session.add(new_user)
     db.session.commit()
     return jsonify({'msg' : 'OK', 'data' : new_user.serialize()})

     

@app.route('/characters', methods=['GET'])
def all_characters():
    characters = Character.query.all()
    all_character = list(map(lambda character: character.serialize(), characters))
    return (
        jsonify({"data": all_character})
    )
@app.route('/planets', methods= ['GET'])
def all_planets():
    planets = Planet.query.all()
    all_planets = list(map(lambda planet : planet.serialize(), planets))
    return (jsonify({"data" : all_planets}))

@app.route('/starships', methods= ['GET'])
def all_starships():
     starships = Starship.query.all()
     all_starships = list(map(lambda starship : starship.serialize(), starships))
     return (jsonify({"data" : all_starships}))

@app.route('/user/<int:id>', methods=['GET'])
def user_id(id):
    users = User.query.get(id)
    if users:
            return jsonify(users.serialize()), 200
    else:
         return jsonify({"error": "User not found"}), 404
    
@app.route('/planet/<int:id>', methods=['GET'])
def planet_id(id):
    planets = Planet.query.get(id)
    if planets:
            return jsonify(planets.serialize()), 200
    else:
         return jsonify({"error": "Planeta no encontrado"}), 404
    
@app.route('/character/<int:id>', methods=['GET'])
def character_id(id):
    characters = Character.query.get(id)
    if characters:
            return jsonify(characters.serialize()), 200
    else:
         return jsonify({"error": "Personaje no encontrado"}), 404

@app.route('/starships/<int:id>', methods=['GET'])
def starship_id(id):
    starships = Starship.query.get(id)
    if starships:
            return jsonify(starships.serialize()), 200
    else:
         return jsonify({"error": "Personaje no encontrado"}), 404




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
