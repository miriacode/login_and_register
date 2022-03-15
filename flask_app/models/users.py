from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash

class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #CREATE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('registro').query_db(query, data)
        return result

    #VALIDATE
    @staticmethod
    def validate_user(user):
        is_valid = True

        if len(user['first_name']) < 3:
            flash('First name should have at least 3 characters', 'register')
            is_valid = False

        if len(user['last_name']) < 3:
            flash('Last name should have at least 3 characters', 'register')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email', 'register')
            is_valid = False
            
        if len(user['password']) < 6:
            flash('Password should have at least 6 characters', 'register')
            is_valid = False
            
        #Bonus ninja:
        if not re.search('[A-Z]', user['password']):
            flash('Invalid password, try including a capital letter', 'register')
            is_valid = False

        if not re.search('[0-9]', user['password']):
            flash('Invalid password, try including a number', 'register')
            is_valid = False

        if user['password'] != user['confirm']:
            flash("Passwords don't match", 'register')
            is_valid = False
        
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('registro').query_db(query, user)
        if len(results) >= 1:
            flash('Email has been registered before', 'registro')
            is_valid = False

        return is_valid

    #READ ONE (by id)
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('registro').query_db(query, data)
        usr = result[0]
        user = cls(usr)
        return user
    
    #READ ONE (by email)
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('registro').query_db(query, data)
        if len(result) < 1:
            return False
        else :
            usr = result[0]
            user = cls(usr)
            return user
