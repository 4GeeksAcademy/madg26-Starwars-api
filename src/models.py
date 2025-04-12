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
            "id": self.id
        }
    

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

class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(String(120), nullable= False)
    gender: Mapped[str]= mapped_column(String(50))
    height: Mapped[int] = mapped_column(Integer)
    favorites_by: Mapped[list['FavoritesCharacter']]= relationship(back_populates = 'characters')

    def serialize(self):
        return {
            "name": self.name,
            "gender" : self.gender,
            "height" : self.height,
            "id" : self.id
        }

class Starship(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(50), nullable = False)
    model: Mapped[str] = mapped_column(String(50))
    favorites_by: Mapped[list['FavoritesStarships']]= relationship(back_populates = 'starships')
    def serialize(self):
        return {
            "name" : self.name,
            "model" : self.name,
            "id" : self.id
        }

class FavoritesPlanets(db.Model):
    __tablename__ = 'favorites_planets'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates = 'like_planet')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
    planets: Mapped['Planet'] = relationship(back_populates = 'favorites_by')

class FavoritesCharacter(db.Model):
    __tablename__ = 'FavoritesCharacter'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates = 'like_character')
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'))
    characters: Mapped['Character'] = relationship(back_populates = 'favorites_by') 

class FavoritesStarships(db.Model):
    __tablename__ = 'FavoritesStarships'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users: Mapped['User'] = relationship(back_populates = 'like_starships')
    starships_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    starships: Mapped['Starship'] = relationship(back_populates = 'favorites_by') 





    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
