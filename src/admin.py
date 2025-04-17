import os
from flask_admin import Admin
from models import db, User, Planet, Character, Starship, FavoritesCharacter, FavoritesStarships, FavoritesPlanets
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import class_mapper, RelationshipProperty

class UserModelView(ModelView):
        column_auto_select_related = True
        column_list = ['id','username', 'email', 'like_planet', 'like_character', 'like_starships']

class FavoritesCharacterModelView(ModelView):
      column_auto_select_related = True
      column_list = ['id', 'users', 'character', 'user_id', 'character_id']
class FavoritesStarshipsModelView(ModelView):
      column_auto_select_related = True
      column_list = ['id', 'users', 'starships', 'user_id', 'starships_id']
class FavoritesPlanetsModelView(ModelView):
      column_auto_select_related = True
      column_list = ['id', 'users', 'planets', 'user_id', 'planet_id']

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Starship, db.session))
    admin.add_view(FavoritesCharacterModelView(FavoritesCharacter, db.session))
    admin.add_view(FavoritesStarshipsModelView(FavoritesStarships, db.session))
    admin.add_view(FavoritesPlanetsModelView(FavoritesPlanets, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))