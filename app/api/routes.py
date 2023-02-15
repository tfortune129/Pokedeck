# from flask import Blueprint, request
# from ..models import User
# from ..apiauthhelper import basic_auth_required, token_auth_required, basic_auth
# from flask_cors import cross_origin


# @api.route('/api/signup', methods=["POST"])
# def signupAPI():

#     data = request.json

#     name = data ['name']
#     username = data['username']
#     email = data['email']
#     password = data['password']

#     print(name, username, email, password)
            
#     #add user to database
#     user = User(name, username, email, password)
#     print(user)

#     user.saveToDB()

#     return {
#      'status': 'ok',
#      'message': "Successfully created your account!"   
#     }


# @api.route('/api/signin', methods=["POST"])
# @basic_auth.login_required
# def getToken():
#     user = basic_auth.current_user()
#     return {
#      'status': 'ok',
#     #  'user': user.to_dict()  
#     }