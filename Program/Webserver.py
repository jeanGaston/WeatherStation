import csv
from datetime import datetime, timedelta
import threading

import requests
from env import *
from flask import Flask, render_template, request
import sqlite3
from database import *
app = Flask(__name__)

# Function to fetch outdoor temperature from Météo-France
def fetch_outdoor_temperature():
    # Format the date in the required format (YYYYMMDD)
    formatted_csv_date = datetime.now().strftime("%Y%m%d%H")
    print(formatted_csv_date)
    # Construct the URL
    url = f"https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/synop.{formatted_csv_date}.csv"

    # Make the HTTP GET request
    response = requests.get(url)
    print(response)
    # Check if request was successful
    try:
        # Decode the content as UTF-8 and split into lines
        lines = response.content.decode('utf-8').splitlines()
        # Read the CSV data using csv.DictReader
        reader = csv.DictReader(lines, delimiter=";")
        
        # Extract outdoor temperature from the CSV data
        for row in reader:
            if row['numer_sta'] == '07149':  #
                outdoor_temp = float(row['t'])
                return round(outdoor_temp - 273.15, 1) #convert °K to °c
    except:
        print("Failed to fetch data from Météo-France.")



# Appel de la fonction pour obtenir la température
temperature = fetch_outdoor_temperature()
print(temperature)

# Route to display the database contents
@app.route('/')
def dashboard():
    data = fetch_all_data()[:5]
    
    return render_template('index.html', data=data, temperature=temperature)

#Route to display the sensor history
@app.route('/history')
def history():
    data = fetch_all_sensor()
    disp_data = []
  
    for mac, name in data:
        disp_data += [fetch_data_by_sensor(name)]


    """ S1 = fetch_data_by_sensor("DEMO1")
    S2 = fetch_data_by_sensor("DEMO2")
    S3 = fetch_data_by_sensor("DEMO3") """
    
    return render_template('history.html', S1=disp_data[0], S2=disp_data[1], S3=disp_data[2])

@app.route('/adm', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Get form data
        old_name = request.form['old_name']
        new_name = request.form['new_name']

        # Update sensor name in the database
        conn = sqlite3.connect(DBFILE)
        c = conn.cursor()
        print(old_name, new_name)
        c.execute("UPDATE Sensors SET Name = ? WHERE mac = ?", (new_name, old_name))
        print()
        conn.commit()
        conn.close()


    data = fetch_all_sensor()
    print(data)
    return render_template('admin.html', data=data, sensors=data)

def run_flask():
    app.run()

def RunInThread_WebServer():
    threading.Thread(target=run_flask, daemon=True).start()
if __name__ == '__main__':
    app.run(debug=True)

