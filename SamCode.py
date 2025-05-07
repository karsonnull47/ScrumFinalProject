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

@app.route('/admin', methods=('GET',))
def admin():
    resers = Reservations.query.all()
    print(resers)
    return render_template('admin.html')

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

