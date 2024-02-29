import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

# load credentials and configuration options from .env file
load_dotenv()  # take environment variables from .env.

# instantiate the app
app = Flask(__name__)




# connect to the database
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')



@app.route("/")
def home():
    """
    Route for the home page
    """
    if 'email' in session:
        return render_template("index.html", logged_in=True)
    return render_template("index.html", logged_in=False)


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

@app.route('/profile')
def profile():
    if 'email' in session:
        user = db.users.find_one({"email": session['email']})
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('show_signin'))


@app.route("/sign_in", methods=["POST"])
def sign_in():
    """
    User sign in route
    """

    email = request.form.get('email')
    password = request.form.get('password')
    if not all([email, password]):
        return redirect(url_for('show_signin'))
    
    user = db.users.find_one({"email": email})

    
    if user and user.get('password') == password:
        session['email'] = user['email']
        return redirect(url_for('home'))
    else:
        return redirect(url_for('show_signin'))





@app.route("/sign_up", methods=["POST"])
def sign_up():
    """
    Post route for user creation of their user
    """

    error_message = ""

    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')

    if not all([email, password, full_name]):
        error_message = "Missing Fields"

    if db.users.find_one({"email": email}):
        error_message = "Email in use"

    #maybe hash it 
    db.users.insert_one({
        "email": email,
        "password": password,
        "full_name": full_name
    })

    if error_message:
        return render_template("sign_up.html", error=error_message)
    else: 
        return redirect(url_for('home'))


    
@app.route('/logout')
def logout():
    """
    User logout route
    """
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    """
    Route to delete the current user's profile
    """
    if 'email' in session:
        email = session['email']
        db.users.delete_one({'email': email})
        session.pop('email', None)  
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")

  
    app.run(port=FLASK_PORT)