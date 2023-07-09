from flask import Flask, request
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId


app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
users = db.users

@app.route('/users', methods=('GET', 'POST'))
@app.route('/users/<_id>', methods=('GET', 'PUT','DELETE'))
def index(_id=None):
    if _id:
        _id = ObjectId(_id)
        if request.method == "GET":
            # getting a user by id and returning it 
            user = users.find_one({'_id':_id})
            if user is not None:
                user = {
                    'name':user['name'],
                    'email':user['email'],
                }
                return user
            else:
                return {"success":False, "message":"Not found!"}
        
        if request.method == "PUT":
            # getting a user by id and updating it 
            # note: password cannot be updated 
            data = request.json
            name = data['name']
            email = data['email']

            newUser = {'name':name, "email":email}
            updateUser = {"$set":newUser}
            user = users.update_one({'_id':_id}, updateUser)
            user = users.find_one({'_id':_id})

            user = {
                'name':user['name'],
                'email':user['email'],
            }
            return user
        
        if request.method == "DELETE":
            # delete the user with given id
            user = users.delete_one({'_id':_id})

            return {"success":True, "message":"User Deleted Successfully!"}
    else:
        if request.method == "GET":
            # return all the users available
            allUsers = list(users.find())
            allUsers = [{
                'name':user['name'],
                'email':user['email'],
            } for user in allUsers]

            return allUsers
        
        if request.method == "POST":
            # create a new user instance
            data = request.json
            name = data['name']
            email = data['email']
            password = data['password']
            

            # hashing the passowrd
            hashed_password = generate_password_hash(password)


            newUser = {
                'name':name,
                "email":email,
                "password":hashed_password
            }
            user = users.insert_one(newUser)

            user = users.find_one({'_id':user.inserted_id})

            user = {
                'name':user['name'],
                'email':user['email'],
            }

            return user

if __name__ == '__main__':
    app.run(debug=True)