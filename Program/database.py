import sqlite3
from os import path

from env import SENSORS, DBFILE

# Function to create the database and tables if they don't exist
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create SensorData table
    c.execute('''CREATE TABLE IF NOT EXISTS Sensors
                (Mac TEXT PRIMARY KEY,
                Name TEXT)''')

    # Create SensorData table
    c.execute('''CREATE TABLE IF NOT EXISTS SensorData
                (Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Sensor TEXT,
                Timestamp TEXT,
                Temp INT,
                HR INTEGER,
                Bat INT,
                FOREIGN KEY (Sensor) REFERENCES Sensors(Name))''')
    
    for mac, name in SENSORS.items():
        # Use INSERT OR IGNORE to prevent duplicates based on primary key
        c.execute("INSERT OR IGNORE INTO Sensors (Mac, Name) VALUES (?, ?)", (mac, name))


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

# Function to fetch data from the database
def fetch_all_data():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT * FROM SensorData ")
    data = c.fetchall()
    conn.close()
    data.reverse()
    return data
# Function to fetch data from the database
def fetch_data_by_sensor(sensor):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT * FROM SensorData WHERE Sensor LIKE ? ", ('%' + sensor + '%',))
    data = c.fetchall()
    conn.close()
    data.reverse()
    return data
# Function to fetch data from the database
def fetch_all_sensor():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT * FROM Sensors ")
    data = c.fetchall()
    conn.close()
    data.reverse()
    return data