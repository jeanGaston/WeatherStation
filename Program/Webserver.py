import threading
from env import *
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
# Function to fetch data from the database
def fetch_all_data():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT * FROM SensorData ")
    data = c.fetchall()
    conn.close()
    data.reverse()
    return data
# Function to fetch data from the database with the sensor name as a parameter
def fetch_data_by_sensor(sensor):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT * FROM SensorData WHERE Sensor LIKE ? ", ('%' + sensor + '%',))
    data = c.fetchall()
    conn.close()
    data.reverse()
    return data
# Route to display the database contents
@app.route('/')
def dashboard():
    data = fetch_all_data()[:5]
    
    return render_template('index.html', data=data)

#Route to display the sensor history
@app.route('/history')
def history():
    S1 = fetch_data_by_sensor("DEMO1")
    S2 = fetch_data_by_sensor("DEMO2")
    S3 = fetch_data_by_sensor("DEMO3")
    
    return render_template('history.html', S1=S1, S2=S2, S3=S3)


def run_flask():
    app.run()

def RunInThread_WebServer():
    threading.Thread(target=run_flask, daemon=True).start()
if __name__ == '__main__':
    app.run(debug=True)

