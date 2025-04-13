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

#----- METODOS PARA LOS USERS-----#
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

@app.route('/user/<int:id>', methods=['PUT'])
def edit_user(id):
     user = User.query.get(id)
     if user is None:
          return jsonify({'msg': 'User no encontrado'}), 400
     data = request.get_json()
     if 'firstname' in data:
          user.firstname = data['firstname']
     if 'username' in data:
          user.username = data['username']
     if 'lastname' in data:
          user.lastname = data['lastname']
     if 'email' in data:
          user.email = data['email']
     if 'password' in data:
          user.password = data['password']
     db.session.commit()
     return ({'msg' : 'Usuario actualizado correctamente', 'usuario' : user.serialize()})

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
     user = User.query.get(id)
     if user is None:
          return jsonify({'msg' : 'Usuario no encontrado'}), 400
     db.session.delete(user)
     db.session.commit()
     user_delete = User.query.all()
     all_user = list(map(lambda user: user.serialize(), user_delete))
      
     return jsonify({'data' : all_user})

@app.route('/user/<int:id>', methods=['GET'])
def user_id(id):
    users = User.query.get(id)
    if users:
            return jsonify(users.serialize()), 200
    else:
         return jsonify({"error": "User not found"}), 404

# ----- METODOS PARA LOS CHARACTERS ----- #
@app.route('/characters', methods=['GET'])
def all_characters():
    characters = Character.query.all()
    all_character = list(map(lambda character: character.serialize(), characters))
    return (
        jsonify({"data": all_character})
    )
@app.route('/character', methods = ['POST'])
def new_character():
     body = request.get_json(silent= True)
     if body is None:
          return ({'msg' : 'Debe enviar la informacion solicitada'}), 400
     if 'name' not in body:
          return jsonify({'msg': 'El campo name es obligatorio'})
     if 'gender' not in body:
          return jsonify({'msg' : 'El campo gender es obligatorio'})
     if 'height' not in body:
          return ({'msg' : 'El campo height es obligatorio'})
     new_character = Character()
     new_character.name = body['name']
     new_character.height = body['height']
     new_character.gender = body['gender']
     db.session.add(new_character)
     db.session.commit()
     return jsonify({'msg' : 'OK', 'data': new_character.serialize()})

@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
     character = Character.query.get(id)
     if character is None:
          return jsonify({'msg' : 'Character no encontrado'}), 400
     db.session.delete(character)
     db.session.commit()
     character_delete = Character.query.all()
     all_character = list(map(lambda character: character.serialize(), character_delete))
      
     return jsonify({'data' : all_character})

@app.route('/character/<int:id>', methods=['GET'])
def character_id(id):
    characters = Character.query.get(id)
    if characters:
            return jsonify(characters.serialize()), 200
    else:
         return jsonify({"error": "Personaje no encontrado"}), 404
    

@app.route('/character/<int:id>', methods=['PUT'])
def edit_character(id):
     character = Character.query.get(id)
     if character is None:
          return jsonify({'msg': 'Character no encontrado'}), 400
     data = request.get_json()
     if 'name' in data:
          character.name = data['name']
     if 'gender' in data:
          character.gender = data['gender']
     if 'height' in data:
          character.height = data['height']
     db.session.commit()
     return ({'msg' : 'Character actualizado correctamente', 'character' : character.serialize()})
    

    
# ----- METODOS PARA LOS PLANETS ----- #
@app.route('/planets', methods= ['GET'])
def all_planets():
    planets = Planet.query.all()
    all_planets = list(map(lambda planet : planet.serialize(), planets))
    return (jsonify({"data" : all_planets}))

@app.route('/planet', methods = ['POST'])
def new_planet():
     body = request.get_json(silent= True)
     if body is None:
          return ({'msg' : 'Debe enviar la informacion solicitada'}), 400
     if 'name' not in body:
          return jsonify({'msg': 'El campo name es obligatorio'})
     if 'climate' not in body:
          return jsonify({'msg' : 'El campo climate es obligatorio'})
     new_planet = Planet()
     new_planet.name = body['name']
     new_planet.climate = body['climate']
     db.session.add(new_planet)
     db.session.commit()
     return jsonify({'msg' : 'OK', 'data': new_planet.serialize()})

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
     planets = Planet.query.get(id)
     if planets is None:
          return jsonify({'msg' : 'Planeta no encontrado'}), 400
     db.session.delete(planets)
     db.session.commit()
     planet_delete = Planet.query.all()
     all_planets = list(map(lambda planet: planet.serialize(), planet_delete))
     return jsonify({'data' : all_planets})

@app.route('/planet/<int:id>', methods=['GET'])
def planet_id(id):
    planets = Planet.query.get(id)
    if planets:
            return jsonify(planets.serialize()), 200
    else:
         return jsonify({"error": "Planeta no encontrado"}), 404
    
@app.route('/planet/<int:id>', methods=['PUT'])
def edit_planet(id):
     planet = Planet.query.get(id)
     if planet is None:
          return jsonify({'msg': 'Planeta no encontrado'}), 400
     data = request.get_json()
     if 'name' in data:
          planet.name = data['name']
     if 'climate' in data:
          planet.climate = data['climate']
     db.session.commit()
     return ({'msg' : 'Planeta actualizado correctamente', 'planeta' : planet.serialize()})
    
# ----- METODOS PARA LOS STARSHIPS ----- #
@app.route('/starships', methods= ['GET'])
def all_starships():
     starships = Starship.query.all()
     all_starships = list(map(lambda starship : starship.serialize(), starships))
     return (jsonify({"data" : all_starships}))

@app.route('/starship', methods = ['POST'])
def new_starship():
     body = request.get_json(silent= True)
     if body is None:
          return ({'msg' : 'Debe enviar la informacion solicitada'}), 400
     if 'name' not in body:
          return jsonify({'msg': 'El campo name es obligatorio'})
     if 'model' not in body:
          return jsonify({'msg' : 'El campo model es obligatorio'})
     new_starship = Starship()
     new_starship.name = body['name']
     new_starship.model = body['model']
     db.session.add(new_starship)
     db.session.commit()
     return jsonify({'msg' : 'OK', 'data': new_starship.serialize()})

@app.route('/starship/<int:id>', methods=['DELETE'])
def delete_starship(id):
     starships = Starship.query.get(id)
     if starships is None:
          return jsonify({'msg' : 'Starship no encontrado'}), 400
     db.session.delete(starships)
     db.session.commit()
     starship_delete = Starship.query.all()
     all_starships = list(map(lambda starship: starship.serialize(), starship_delete))
     return jsonify({'data' : all_starships})

@app.route('/starships/<int:id>', methods=['GET'])
def starship_id(id):
    starships = Starship.query.get(id)
    if starships:
            return jsonify(starships.serialize()), 200
    else:
         return jsonify({"error": "Personaje no encontrado"}), 404

@app.route('/starship/<int:id>', methods=['PUT'])
def edit_starship(id):
     starship = Starship.query.get(id)
     if starship is None:
          return jsonify({'msg': 'Vehiculo no encontrado'}), 400
     data = request.get_json()
     if 'name' in data:
          starship.name = data['name']
     if 'model' in data:
          starship.model= data['model']
     db.session.commit()
     return ({'msg' : 'Vehiculo actualizado correctamente', 'sttarship' : starship.serialize()})



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
