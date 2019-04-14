
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)

app.debug = True

db = client.app

# default routing provies reference to all routes
@app.route("/")
def hello():
	return 'Please follow links to make use of Mongo Database: <br>' \
		'1. /get/ - get all users <br>' \
		'3. /username/ - get particular user <br>' \
		'2. /delete/username/ - delete user with username <br>' \
		'3. /insert/username/firstname/lastname/ - insert user <br>' \

# getting all registered user data
# e.g. http://localhost:5000/get/
@app.route("/get/")
def get_data():
	users = db.users.find()
	data = 'Name of Users: <br>'
	for user in users:
		data = data + user['username'] + ': ' \
		+ user['firstname'] + user['lastname'] + '<br>'
	return data

# insert user with username, firstname and password
# e.g. http://localhost:5000/insert/jeevan/Jeevan/Pant/
@app.route("/insert/")
@app.route("/insert/<username>/<firstname>/<lastname>/")
def insert_data(username=None, firstname=None, lastname=None):
	if username != None and firstname != None and lastname != None:
		db.users.insert_one({
			"username": username,
			"firstname": firstname,
			"lastname": lastname,
		})
		return 'Data inserted successfully: ' +  username + ', ' \
		+ firstname + ' ' + lastname
	else:
		return 'Data insufficient. Please try again!'

# delete user
# e.g. http://localhost:5000/remove/jeevan/Jeevan/Pant/
@app.route("/insert/")
@app.route("/delete/")
@app.route("/delete/<username>/")
def delete_data(username=None):
	if username != None:
		db.users.remove({
			"username": username,
		})
		return 'Data delected successfully with useraname: ' +  username
	else:
		return 'Provide data to delete. Please try again!'

# get specific user
# e.g. http://localhost:5000/jeevan/
@app.route("/<username>/")
def users(username):
	try:
		user = db.users.find_one({'username': username})
		return user['firstname'] + ' ' + user['lastname']
	except:
		return "User couldn't be found"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)