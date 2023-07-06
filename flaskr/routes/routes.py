from flask import Blueprint, request
from ..controller.user_controllers import UserController
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    # Call controller method to handle GET request
    return UserController.get_users()

@user_bp.route('/users', methods=['POST'])
@user_bp.route('/login', methods=['POST'])
def do_login():
    # Call controller method to handle POST request
    return UserController.do_login()

@user_bp.route('/signup', methods=['POST'])
def do_signup():
    # Call controller method to handle POST request
    return UserController.do_signup()

@user_bp.get('/profile')
@jwt_required()
def get_profile():
    # Call controller method to handle POST request
    return UserController.get_profile()
