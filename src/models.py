from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique= True, nullable= False)
    password: Mapped[str] = mapped_column(String(16), nullable=False)
    firstname: Mapped[str] = mapped_column(String(25), nullable= False)
    lastname: Mapped[str] = mapped_column(String(25), nullable = False)
    email: Mapped[str] = mapped_column(String(25), unique= True, nullable= False)
    like_planet: Mapped[list['FavoritesPlanets']] = relationship(back_populates = 'users')
    like_character: Mapped[list['FavoritesCharacter']] = relationship(back_populates = 'users')
    like_starships: Mapped[list['FavoritesStarships']] = relationship(back_populates = 'users')

    def serialize(self):
        return {
            "firstname" : self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "email": self.email,
            "id": self.id,
            "like_character" : list(map(lambda like_character: like_character.serialize(), self.like_character)),
            "like_starships": list(map(lambda like_starships: like_starships.serialize(), self.like_starships)),
            "like_planet": list(map(lambda like_planet: like_planet.serialize(), self.like_planet))
        }
    def __repr__(self):
        return f'{self.username}'
    

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(120), nullable = False)
    climate: Mapped[str] = mapped_column(String(50))
    favorites_by: Mapped[list['FavoritesPlanets']] = relationship(back_populates = 'planets')

    def serialize(self): 
        return{
            "name" : self.name,
            "climate" : self.climate,
            "id": self.id
        }
    def __repr__(self):
        return f'{self.name}'

class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(String(120), nullable= False)
    gender: Mapped[str]= mapped_column(String(50))
    height: Mapped[int] = mapped_column(Integer)
    favorites_by: Mapped[list['FavoritesCharacter']]= relationship(back_populates = 'character')

    def serialize(self):
        return {
            "name": self.name,
            "gender" : self.gender,
            "height" : self.height,
            "id" : self.id
        }
    def __repr__(self):
        return f'{self.name}'

class Starship(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(50), nullable = False)
    model: Mapped[str] = mapped_column(String(50))
    favorites_by: Mapped[list['FavoritesStarships']]= relationship(back_populates = 'starships')
    def serialize(self):
        return {
            "name" : self.name,
            "model" : self.model,
            "id" : self.id
        }
    def __repr__(self):
        return f'{self.name}'

class FavoritesPlanets(db.Model):
    __tablename__ = 'favorites_planets'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates = 'like_planet')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
    planets: Mapped['Planet'] = relationship(back_populates = 'favorites_by')
    def __repr__(self):
        return f'{self.planets.name}'

    def serialize(self):
        return {
            'planet_name' : self.planets.name,
            'planet_id' : self.planets.id,
            'planet_climate' : self.planets.climate

        }
class FavoritesCharacter(db.Model):
    __tablename__ = 'FavoritesCharacter'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates = 'like_character')
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'))
    character: Mapped['Character'] = relationship(back_populates = 'favorites_by') 
    def __repr__(self):
        return f'{self.character.name}'
    def serialize(self):
        return {
            'character_name' : self.character.name,
            'character_id' : self.character.id,
            'character_gender' : self.character.gender,
            'character_height': self.character.height
        }
   

class FavoritesStarships(db.Model):
    __tablename__ = 'FavoritesStarships'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates = 'like_starships')
    starships_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    starships: Mapped['Starship'] = relationship(back_populates = 'favorites_by') 
    def __repr__(self):
        return f'{self.starships.name}'
    def serialize(self):
        return {
            'starship_model' : self.starships.model,
            'starship_name' : self.starships.name,
            'starship_id' : self.starships.id
        }


