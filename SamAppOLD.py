#import modules
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#create a flask app object and set app variables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'reservations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'your_secret_key'

def get_db_connection():
    user = 'root'
    password = 'password'
    host = '127.0.0.1'
    port = 5008
    database = 'Reservations'
    

class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passengerName = db.Column(db.String(200), nullable=False)
    seatRow = db.Column(db.Integer, primary_key=True)
    seatColumn = db.Column(db.Integer, primary_key=True)
    eTicketNumber = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, nullable=True)
    def __repr__(self):
        return f'<Reservations {self.passengerName}>'

#use app.route to create a flask view for the index page of the web app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=('POST',))
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

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    #get the task based on the id
    res = Reservations.query.get_or_404(id)
    #delete the task
    
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('admin'))

#run the application
app.run(port=5008, debug=True)

