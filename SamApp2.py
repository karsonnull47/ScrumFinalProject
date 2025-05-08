#import modules
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import URL
from datetime import datetime
import os

#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

#create a connection object to the module2 database
def get_db_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            "root", "root", "localhost", 5008, "reservations"
        )
    )

#use app.route to create a flask view for the index page of the web app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=('POST',))
def admin():
    return render_template('admin.html')
def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix
def admin_post():
    #get data submitted from the form (report type and year)
    userID = request.form.get('userID')
    password = request.form.get('password')

    #create a connection to the database to query it
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    #validate user selected something for all fields.
    if not userID:
        flash("ERROR: User ID required.")
        return redirect(url_for('admin.html'))

    if not year:
        flash("ERROR: Password required.")
        return redirect(url_for('admin.html'))

    admin_query = "sql goes here (match on ID and password)"
    cursor.execute(admin_query, (userID, password,))
    admin_result = cursor.fetchall()

    if #check curser...  If no records, they're not an admin
        flash("ERROR: Invalid name/password.")
        return redirect(url_for('admin.html'))

    #if you got here, they're an admin, so...

    #create an empty result variable to send back to the admin page if there are no reservations.
    #If we don't do this, reloading the form throws UnboundLocalError
    reservations_result = None

    reservations_query = "SQL to get reservations"
    cursor.execute(reservations_query, (year,))
    reservations_result = cursor.fetchall()

    #send reservations list to the admin.html template
    return render_template('admin.html', reservations_result = reservations_result)

@app.route('/reservations', methods=('GET',))
def reservations():
    return render_template('reservations.html')

#Processes navigation page with POST request
@app.route('/', methods=('POST',))
def index_post():
    #get the form data
    option = request.form.get('option')

    #determine which view to send the application to
    if option == "admin":
        return redirect(url_for('admin'))
    elif option == "reservations":
        return redirect(url_for('reservations'))
    elif option == "index":
        return redirect(url_for('index'))
    else:
        flash("ERROR: You must choose an option from the menu")
        return redirect(url_for('navigation'))

#run the application
app.run(port=5008, debug=True)

