#import modules
from flask import Flask, render_template, request, flash, url_for, redirect

#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

#create a connection object to the module2 database
def get_db_connection():

    return mydb

#use app.route to create a flask view for the index page of the web app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=('GET',))
def admin():
    return render_template('admin.html')

@app.route('/reservations', methods=('GET',))
def reservations():
    return render_template('reservations.html')


#run the application
app.run(port=5008, debug=True)

