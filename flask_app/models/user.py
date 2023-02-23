from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class User:
    DB = 'login'

    def __init__(self, data):
        self.first_name = data['f_name']
        self.last_name = data['l_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.id = data['id']

    @classmethod
    def create_user(cls, data):
        if not cls.validate_input(data):
            return False
        pdata = User.parse_data(data)
        print("Data has been parsed.")
        query = """INSERT INTO user (f_name, l_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        print("Data has been saved.")
        user_id = connectToMySQL(cls.DB).query_db(query, pdata)
        session['user_id'] = user_id
        print("User has been created.")
        return True

    # READ login.user SQL
    
    @classmethod
    def user_email(cls, email):
        data = {'email':email}
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if result:
            result = cls(result[0])
        return result

    @staticmethod
    def validate_input(data):
        EMAIL_REGEX =  re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['f_name']) < 3: # VALIDATE LENGTH OF FIRST NAME
            flash("First name must contain letters only and be at least 2 characters long.", "reg")
            is_valid = False
        if len(data['l_name']) < 3: # VALIDATE LENGTH OF LAST NAME
            flash("Last name must contain letters only and be at least 2 characters long.", "reg")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): # NEED TO ALSO CHECK IF EMAIL ALREADY EXISTS
            flash("Invalid email address. Please try again.", "reg")
            is_valid = False
        if User.user_email(data['email'].lower()):
            flash("That email has already been taken. Please use another email.", "reg")
            is_valid = False
        if len(data['password']) < 8: # VALIDATE LENGTH OF PW
            flash("Password must be at least 8 characters long.", "reg")
            is_valid = False
        if data['password'] != data['confirm_password']: # VALIDATE IF BOTH FIELDS OF PW AND CONFIRM PW MATCH
            flash("Passwords do not match. Please try again.", "reg")
            is_valid = False
        return is_valid
    
    @staticmethod
    def parse_data(data):
        print("Parsing data...")
        parsed_data = {}
        parsed_data['first_name'] = data['f_name']
        parsed_data['last_name'] = data['l_name']
        print("hi")
        parsed_data['email'] = data['email'].lower()
        print("ew")
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        print(parsed_data)
        return parsed_data
    
    @staticmethod
    def login(data):
        user = User.user_email(data['email'].lower())
        if user:
            if bcrypt.check_password_hash(user.password, data['password']):
                session['user_id'] = user.id
                return True
        flash("Your login is incorrect. Please try again.", "login")
        return False