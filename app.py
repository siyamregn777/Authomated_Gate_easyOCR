#app.py

from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

def init_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='Registration'  # Updated database name
    )
    c = conn.cursor()
    
    # Create Drivers table
    c.execute('CREATE TABLE IF NOT EXISTS drivers (id_number VARCHAR(255) PRIMARY KEY)')
    
    # Create License Plates table
    c.execute('CREATE TABLE IF NOT EXISTS plates (plate VARCHAR(255) PRIMARY KEY, id_number VARCHAR(255), FOREIGN KEY (id_number) REFERENCES drivers (id_number) ON DELETE CASCADE)')
    
    conn.commit()
    conn.close()

@app.route('/check_plate', methods=['GET'])
def check_plate():
    plate = request.args.get('plate')
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='Registration'  # Updated database name
    )
    c = conn.cursor()
    c.execute('SELECT * FROM plates WHERE plate = %s', (plate,))
    result = c.fetchone()
    conn.close()
    return jsonify({"registered": result is not None})

@app.route('/register_plate', methods=['POST'])
def register_plate():
    id_number = request.form['id_number']
    plate = request.form['plate']
    
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='Registration'  # Updated database name
    )
    c = conn.cursor()

    # Check if the driver exists
    c.execute('SELECT * FROM drivers WHERE id_number = %s', (id_number,))
    driver = c.fetchone()
    
    if driver is None:
        # If the driver does not exist, create a new driver entry
        c.execute('INSERT INTO drivers (id_number) VALUES (%s)', (id_number,))
    
    # Check for existing license plates
    c.execute('SELECT * FROM plates WHERE plate = %s', (plate,))
    if c.fetchone() is not None:
        conn.close()
        return jsonify({"message": "License Plate already registered!"}), 400

    c.execute('INSERT INTO plates (plate, id_number) VALUES (%s, %s)', (plate, id_number))
    conn.commit()
    conn.close()
    return jsonify({"message": "License Plate Registered!"}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)