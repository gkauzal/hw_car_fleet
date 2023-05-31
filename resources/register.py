from flask_restful import Resource, reqparse
from models.user import UserModel
from passlib.hash import pbkdf2_sha512


class UserRegister(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('username',
                      type=str,
                      required=True,
                      help='This field cannot be left blank')
  parser.add_argument('password',
                      type=str,
                      required=True,
                      help='This field cannot be left blank')

  def post(self):
    data = UserRegister.parser.parse_args()
    if UserModel.find_by_attribute(username=data['username']):
      return {'message': 'A user with that username already exists'}, 400

    # user = UserModel(data['username'], data['password'])

    password = pbkdf2_sha512.using(rounds=310000,
                                   salt_size=20).hash(data['password'])
    user = UserModel(data['username'], password)
    user.save_to_db()

    return {'message': 'User created successfully.'}, 201
