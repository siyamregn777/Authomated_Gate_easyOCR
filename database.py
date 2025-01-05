#database.py
import mysql.connector

def init_db():
    conn = mysql.connector.connect(
        host='localhost',  
        user='root',  
        password='root',
        database='Registration'  # Updated database name
    )
    c = conn.cursor()
    
    # Create Drivers table
    c.execute('CREATE TABLE IF NOT EXISTS drivers (id_number VARCHAR(255) PRIMARY KEY)')
    
    # Create License Plates table
    c.execute('CREATE TABLE IF NOT EXISTS plates (plate VARCHAR(255) PRIMARY KEY, id_number VARCHAR(255), FOREIGN KEY (id_number) REFERENCES drivers (id_number) ON DELETE CASCADE)')
    
    conn.commit()
    conn.close()