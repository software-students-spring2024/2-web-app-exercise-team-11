import os
import datetime
from flask import Flask, render_template, request, redirect, url_for

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

@app.route("/sign_up", methods=["POST"])
def sign_up():
    """
    Route for user sign up. 
    """

    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')

    # if not all([email, password, full_name]):
    #     return jsonify({'message': 'Missing fields'}), 400

    return render_template("sign_up.html")



if __name__ == "__main__":
    # use the PORT environment variable, or default to 5000
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")

    # import logging
    # logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=FLASK_PORT)