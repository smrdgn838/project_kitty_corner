from flask_app import app
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.kitty import Kitty
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.kitties = []


    @classmethod
    def create_user(cls,data):
        query = '''INSERT INTO users (first_name, last_name, email, password)
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );
                '''
        return connectToMySQL("kitty_lovers_schema").query_db(query,data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL("kitty_lovers_schema").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod  #this gets ONE user, all kitties associated with that user
    def get_by_id(cls,data):
        query = '''SELECT * from users 
                LEFT JOIN kitties 
                ON users.id = kitties.user_id
                WHERE users.id = %(id)s;
                '''
        results = connectToMySQL("kitty_lovers_schema").query_db(query,data)
        if results:
            user = cls(results[0])
            for row in results:
                kitties_data = {
                    "id": row["kitties.id"],
                    "age_range": row["age_range"],
                    "breed": row["breed"],
                    "personality": row["personality"],
                    "other_pets": row["other_pets"],
                    "created_at": row["kitties.created_at"],
                    "updated_at": row["kitties.updated_at"],
                    "user_id": row["id"]
                }
                user.kitties.append(Kitty(kitties_data))
            return user


    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) < 2:
            flash("First name must be more than 2 characters!!")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be more than 2 characters!!")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email!!")
        if len(user["password"]) < 8 or len(user["password"]) > 30:
            flash("Password must be between 8 and 30 characters!!")
            is_valid = False
        return is_valid 



