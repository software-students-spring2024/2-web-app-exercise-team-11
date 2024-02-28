import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

# load credentials and configuration options from .env file
load_dotenv()  # take environment variables from .env.

# instantiate the app
app = Flask(__name__)


# connect to the database
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]  # store a reference to the database


@app.route("/")
def home():
    """
    Route for the home page
    """
    return render_template("index.html")


@app.route('/sign_up')
def show_signup():
    """
    Route for the sign up page
    """
    return render_template('sign_up.html')

@app.route('/sign_in')
def show_signin():
    """
    Route for the sign in page
    """
    return render_template("sign_in.html")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    """
    User sign in route
    """

    email = request.form.get('email')
    password = request.form.get('password')
    if not all([email, password]):
        return jsonify({'message': 'Missing fields'}), 400
    
    user = db.users.find_one({"email": email})

    if user and user['password'] == password:
        #Check session stuff
        return redirect(url_for('home'))
    else:
        return jsonify({'message': 'Incorrect Password'}), 400




@app.route("/sign_up", methods=["POST"])
def sign_up():
    """
    Post route for user creation of their user
    """

    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')

    if not all([email, password, full_name]):
        return jsonify({'message': 'Missing fields'}), 400

    if db.users.find_one({"email": email}):
        return jsonify({'message': 'Email already in use'}), 400

    #maybe hash it 
    db.users.insert_one({
        "email": email,
        "password": password,
        "full_name": full_name
    })
    


    return redirect(url_for('home'))




if __name__ == "__main__":
    # use the PORT environment variable, or default to 5000
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")

    # import logging
    # logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=FLASK_PORT)