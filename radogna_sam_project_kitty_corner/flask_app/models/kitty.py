from flask_app import app
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user



class Kitty:
    def __init__(self, data):
        self.id = data['id']
        self.age_range = data['age_range']
        self.breed = data['breed']
        self.other_pets = data['other_pets']
        self.personality = data['personality']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None


    @classmethod
    def create_kitty(cls,data):
        query = '''INSERT INTO kitties (age_range, breed, personality, other_pets, user_id)
                VALUES ( %(age_range)s, %(breed)s,  %(personality)s, %(other_pets)s, %(user_id)s );
                '''
        return connectToMySQL("kitty_lovers_schema").query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = '''SELECT * FROM kitties
                LEFT JOIN users
                ON kitties.user_id = users.id;
                '''
        results = connectToMySQL("kitty_lovers_schema").query_db(query)
        kitties = []
        for kitty in results:
            this_kitty = cls(kitty)
            user_data = {
                "id": kitty["users.id"],
                "first_name": kitty["first_name"],
                "last_name": kitty["last_name"],
                "email": kitty["email"],
                "password": kitty["password"],
                "created_at": kitty["users.created_at"],
                "updated_at": kitty["users.updated_at"]
            }
            this_kitty.user = user.User(user_data)
            kitties.append(this_kitty)
        return kitties

    
    @classmethod
    def get_by_id(cls,data):
        query = '''SELECT * FROM kitties 
                LEFT JOIN users
                ON kitties.user_id = users.id
                WHERE kitties.id = %(id)s;
                '''
        results = connectToMySQL("kitty_lovers_schema").query_db(query,data)
        print(results)
        kitty = cls(results[0])
        results = results[0]
        data = {
                "id": results["users.id"],
                "first_name": results["first_name"],
                "last_name": results["last_name"],
                "email": results["email"],
                "password": results["password"],
                "created_at": results["users.created_at"],
                "updated_at": results["users.updated_at"]
            }
        kitty.user = user.User(data)
        return kitty
        
    
    @classmethod
    def update_kitty(cls,data):
        query = '''UPDATE kitties SET
                age_range = %(age_range)s, breed = %(breed)s, personality = %(personality)s, other_pets = %(other_pets)s
                WHERE id = %(id)s;
                '''
        return connectToMySQL("kitty_lovers_schema").query_db(query,data)
    
    @classmethod
    def delete_kitty(cls,data):
        query = 'DELETE FROM kitties WHERE id = %(id)s;'
        return connectToMySQL("kitty_lovers_schema").query_db(query,data)



    @staticmethod
    def validate_kitty(kitty):
        is_valid = True
        if len(kitty["age_range"]) < 1:
            flash("Woops, your kitty has no age range!!")
            is_valid = False
        if len(kitty["breed"]) < 2:
            flash("Woops, your 'breed' response was too short!!")
            is_valid = False
        if len(kitty["personality"]) < 2:
            flash("Woops, your 'personality' response was too short!!")
            is_valid = False
        if len(kitty["other_pets"]) < 1:
            flash("Woops, you need to let us know if you have other pets!!")
            is_valid = False
        return is_valid 