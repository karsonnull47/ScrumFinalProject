#import modules
from flask import Flask, render_template, request, flash, url_for, redirect
import sqlite3

#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

#create a connection object to the module2 database
def get_db_connection():
    mydb = sqlite3.connect('reservations.db')
    mydb.row_factory = sqlite3.Row
    return mydb

#use app.route to create a flask view for the index page of the web app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=('GET',))
def admin():
    return render_template('admin.html')



@app.route('/reservations', methods=('GET','POST'))
def reservations():
    conn = get_db_connection()

    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        row = int(request.form['seat_row']) - 1  
        col = int(request.form['seat_column']) - 1

        #creating a ticket number that matches the format already in the database.
        def generate_eticket_number(first, last):
            base = "INFOTC4320"
            combined = first + last
            result = ""
            for i in range(max(len(base), len(combined))):
                if i < len(combined):
                    result += combined[i]
                if i < len(base):
                    result += base[i]
            return result
        
        eticket = generate_eticket_number(first,last)
        
        # Check if seat is taken
        existing = conn.execute(
            'SELECT * FROM reservations WHERE seatRow = ? AND seatColumn = ?',
            (row, col)
        ).fetchone()

        if existing:
            flash('That seat is already reserved.', 'error')
        else:
            name = f"{first} {last}"
            conn.execute(
                'INSERT INTO reservations (seatRow, seatColumn, passengerName, eTicketNumber) VALUES (?, ?, ?, ?)',
                (row, col, name, eticket)
            )
            conn.commit()
            flash('Seat successfully reserved!', 'success')

    reservations = conn.execute(
        'SELECT seatRow, seatColumn, passengerName FROM reservations'
    ).fetchall()

    # Create the seating chart
    seating_chart = [['' for _ in range(4)] for _ in range(12)]
    for res in reservations:
        seating_chart[res['seatRow']][res['seatColumn']] = "Occupied"

    return render_template('reservations.html', seating_chart=seating_chart)



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

