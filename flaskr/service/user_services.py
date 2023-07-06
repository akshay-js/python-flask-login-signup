from flask import g
from ..db import get_connection_string, get_db
import bcrypt
from flask import request
from flask import jsonify
import pyodbc

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

class UserService:
    @staticmethod
    def get_users():
        # Perform logic to retrieve users from the database or any other data source
        # Return the users
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        # Process and format the users as needed
        formatted_users = [dict(user) for user in users]

        cursor.close()

        return {'users': formatted_users}

    @staticmethod
    def do_login():
        email = request.json.get('email')
        password = request.json.get('password')
        print(email, password)

        try:
            conn = pyodbc.connect(get_connection_string())
            print(conn)
            cursor = conn.cursor()

            print(password)
            cursor.execute('SELECT password FROM users WHERE email=?', (email,))
            result = cursor.fetchone()
            print(result)
            #   conn.commit()
            conn.close()

            if not result :
                print('in the if ')
                return jsonify(message='Invalid credentials'), 401
            if result is None:
                print('in the if 2')
                return jsonify(message='Invalid credentials'), 401

            hashed_password = result[0]
            print(hashed_password)

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                access_token = create_access_token(identity=email)
                return jsonify(access_token=access_token), 201
            else:
                return jsonify(message='Invalid credentials'), 401
        except pyodbc.Error as error:
            return jsonify(message=str(error)), 500

    @staticmethod
    def do_signup():
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        try:
            conn = pyodbc.connect(get_connection_string())
            cursor = conn.cursor()

            # Check if the email is already registered
            cursor.execute('SELECT id FROM users WHERE email=?', (email,))
            result = cursor.fetchone()
            if result:
                conn.close()
                return jsonify(message='Email already registered'), 409

            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(password.encode('utf-8'), salt)
            # Insert the new user into the database
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            conn.close()

            return jsonify(message='User registered successfully'), 201
        except pyodbc.Error as e:
            return jsonify(message=str(e)), 500

    @staticmethod
    def get_profile():
        current_user = get_jwt_identity()
        print(str(current_user))
        try:
            conn = pyodbc.connect(get_connection_string())
            cursor = conn.cursor()
            cursor.execute('select * from users where email=?', (str(current_user)))
            result = cursor.fetchone()
            print(result)
            if not result:
                conn.close()
                return jsonify(message='User not found'), 404
            print(result[0])
            user_profile = {
                'id': result[0],
                'email': result[1],
            }
            conn.close()

            return jsonify(user_profile), 200
        except  pyodbc.Error as e:
            return jsonify(message=str(e)), 500

