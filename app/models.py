from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()
# do joins table
# catchpokemon.db.table

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique = True)
    email = db.Column(db.String(150), nullable=False, unique = True)
    password = db.Column(db.String, nullable=False)

    # post = db.relationship("Post", backref='author', lazy = True)
    # attribute here to catch po`kemon

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    # add to database and commit
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'apitoken': self.apitoken
            

        }

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ability = db.Column(db.String)
    sprite = db.Column(db.String)
    hp_stat = db.Column(db.Integer)
    attack_stat = db.Column(db.Integer)
    defense_stat = db.Column(db.Integer)
    move = db.Column(db.String)
    caught = False


    def __init__(self, name, ability, sprite, hp_stat, attack_stat, defense_stat, move):
        self.name = name
        self.ability = ability
        self.sprite = sprite
        self.hp_stat = hp_stat
        self.attack_stat = attack_stat
        self.defense_stat = defense_stat
        self.move = move
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
    def saveChanges(self):
        db.session.commit()



class Catch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)


    def __init__(self, user_id, pokemon_id):
       self.user_id = user_id
       self.pokemon_id = pokemon_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()


# classes to make:
# pokemon

# pokemongroup

# make decision on how i want to catch pokemon and teams before i do flask migrate and flask upgrade

# login, signup, landing, search, user (where teams are), battle page (where you will set how to win)