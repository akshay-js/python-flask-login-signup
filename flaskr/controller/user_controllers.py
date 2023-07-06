from flask import request
from ..service.user_services import UserService

class UserController:
    @staticmethod
    def get_users():
        # Call service method to get users
        users = UserService.get_users()
        # Process and format the users as needed
        return {'users': users}

    @staticmethod
    def create_user(user_data):
        # Call service method to create a user
        created_user = UserService.get_users()
        # Process and format the created user as needed
        return {'user': created_user}

    @staticmethod
    def do_login():
        return UserService.do_login()

    @staticmethod
    def do_signup():
        return UserService.do_signup()

    @staticmethod
    def get_profile():
        return UserService.get_profile()
