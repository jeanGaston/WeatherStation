from datetime import datetime
import sqlite3
from os import path
import plotly.graph_objs as go
import pandas as pd



from env import *

# Function to create the database and tables if they don't exist
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create SensorData table
    c.execute('''CREATE TABLE IF NOT EXISTS Sensors
                (Mac TEXT PRIMARY KEY,
                Name TEXT)''')
    for mac, name in SENSORS.items():
        # Use INSERT OR IGNORE to prevent duplicates based on primary key
        c.execute("INSERT OR IGNORE INTO Sensors (Mac, Name) VALUES (?, ?)", (mac, name))
    # Create SensorData table
    c.execute('''CREATE TABLE IF NOT EXISTS SensorData
                (Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Sensor TEXT,
                Timestamp TEXT,
                Temp INT,
                HR INT,
                Bat INT,
                FOREIGN KEY (Sensor) REFERENCES Sensors(Name))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS alert_settings (
                id INTEGER PRIMARY KEY,
                smtp_id TEXT,
                smtp_pwd TEXT,
                smtp_server TEXT,
                smtp_port INTEGER,
                recipient_email TEXT,
                MAX_HR INT
                MAX_TEMP);''')
    c.execute("INSERT OR IGNORE INTO alert_settings (smtp_id, smtp_pwd, smtp_server, smtp_port, recipient_email, MAX_HR, MAX_TEMP) VALUES (?, ?, ?, ?, ?, ?, ?)", (SMTP_ID, SMTP_PWD, SMTP, SMTP_PORT, RECIPIENT, MAX_HR, MAX_TEMP))



    conn.commit()
    conn.close()

# Check if the database file exists
def check_database(db_name):
    if not path.exists(db_name):
        
        print(f"[{datetime.now()}] DB - Database '{db_name}' not found. Creating...")
        create_database(db_name)
        print(f"[{datetime.now()}] DB - Database and tables created successfully.")
    else:
        print(f"[{datetime.now()}] DB - Database '{db_name}' found.")


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

def update_sensor_settings(new_name, old_name):
    # Update sensor name in the database
            conn = sqlite3.connect(DBFILE)
            c = conn.cursor()
            c.execute("UPDATE Sensors SET Name = ? WHERE mac = ?", (new_name, old_name))
            conn.commit()
            conn.close()

# Function to fetch email settings from the database
def fetch_email_settings():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT smtp_id, smtp_pwd, smtp_server, smtp_port, recipient_email FROM alert_settings")
    settings = c.fetchone()
    conn.close()
    return settings
# Function to fetch MAX HR and  MAX temp  from the database
def fetch_threshold_settings():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT MAX_HR, MAX_TEMP FROM alert_settings")
    settings = c.fetchone()
    conn.close()
    return settings

# Function to update email settings in the database
def update_email_settings(smtp_id, smtp_pwd, smtp_server, smtp_port, recipient_email):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("UPDATE alert_settings SET smtp_id = ?, smtp_pwd = ?, smtp_server = ?, smtp_port = ?, recipient_email = ? ", (smtp_id, smtp_pwd, smtp_server, smtp_port, recipient_email))
    conn.commit()
    print(f"[{datetime.now()}] Web -  Mail settings updated :")
    print_email_settings()
    conn.close()

# Function to update threshold settings in the database
def update_threshold_settings(max_hr, max_temp):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("UPDATE alert_settings SET smtp_id = ?, smtp_pwd = ? ", (smtp_id, smtp_pwd, smtp_server, smtp_port, recipient_email))
    conn.commit()
    print(f"[{datetime.now()}] Web -  Mail settings updated :")
    print_email_settings()
    conn.close()

def print_email_settings():
    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    # Fetch email settings
    c.execute("SELECT * FROM alert_settings")
    settings = c.fetchone()

    # Print settings
    if settings:
        print("Email Settings:")
        print(f"Sender Email: {settings[1]}")
        print(f"SMTP pwd:{settings[2]}")
        print(f"SMTP Server: {settings[3]}")
        print(f"SMTP Port: {settings[4]}")
        print(f"Recipient Email: {settings[5]}")
    else:
        print("No email settings found in the database.")

    # Close the connection
    conn.close()

def history_graph_temp():
    # Fetch sensor data
    sensorList = fetch_all_sensor()
    Trace = ['','' ,'' ]
    i =0
    for mac, name in sensorList:

        data = fetch_data_by_sensor(name)
        #print(data)
        df = pd.DataFrame(data, columns=['ID', 'Sensor', 'Timestamp', 'Temp', 'HR', 'Bat'])
        # Create traces for temperature
        Trace[i] = go.Scatter(x=df['Timestamp'], y=df['Temp'], mode='lines', name=name)
        #print(Trace[i])
        i+=1
        #print(trace_temp)
    # Create layout
    layout = go.Layout(title='Graph Temp history',
                       xaxis=dict(title='Time'),
                       yaxis=dict(title='Temperature in °C'))

    # Create figure
    fig = go.Figure(data=[Trace[0], Trace[1], Trace[2] ], layout=layout )

    # Convert figure to JSON for rendering in template
    graph_json = fig.to_json()
    #print(graph_json)
    return graph_json
def history_graph_HR():
    # Fetch sensor data
    sensorList = fetch_all_sensor()
    Trace = ['','','']
    i = 0
    
  
    for mac, name in sensorList:
        
        data = fetch_data_by_sensor(name)
        df = pd.DataFrame(data, columns=['ID', 'Sensor', 'Timestamp', 'Temp', 'HR', 'Bat'])
        # Create traces for temperature
        Trace[i] = go.Scatter(x=df['Timestamp'], y=df['HR'], mode='lines', name=name)
        #print(Trace[i])
        i+=1

        
        #print(trace_temp)
    # Create layout
    layout = go.Layout(title='Graph HR history',
                       xaxis=dict(title='Time'),
                       yaxis=dict(title='Humidity Rate in % '))

    # Create figure
    fig = go.Figure(data=[Trace[0], Trace[1], Trace[2] ], layout=layout )

    # Convert figure to JSON for rendering in template
    graph_json = fig.to_json()
    #print(graph_json)
    return graph_json