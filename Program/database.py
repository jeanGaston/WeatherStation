import sqlite3
from os import path

# Function to create the database and tables if they don't exist
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create SensorData table
    c.execute('''CREATE TABLE IF NOT EXISTS SensorData
                 (Id INTEGER PRIMARY KEY AUTOINCREMENT,
                  FOREIGN KEY (Sensor) REFERENCES Sensors(Name),
                  Timestamp TEXT,
                  Temp INT,
                  HR INTEGER,
                  Bat INT)''')

    # Create Sensors table
    c.execute('''CREATE TABLE IF NOT EXISTS Sensors
                 (Mac TEXT RIMARY KEY,
                  Name TEXT )''')

    conn.commit()
    conn.close()

# Check if the database file exists
def check_database(db_name):
    if not path.exists(db_name):
        print(f"Database '{db_name}' not found. Creating...")
        create_database(db_name)
        print("Database and tables created successfully.")
    else:
        print(f"Database '{db_name}' found.")


# Function to add data to SensorData table
def add_sensor_data(db_name, sensor, timestamp, temp, hr, bat):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''INSERT INTO SensorData (Sensor, Timestamp, Temp, HR, Bat)
                 VALUES (?, ?, ?, ?, ?)''', (sensor, timestamp, temp, hr, bat))

    conn.commit()
    conn.close()