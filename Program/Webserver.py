import csv
from datetime import datetime, timedelta
import threading

import requests
from env import *
from flask import Flask, redirect, render_template, request
import sqlite3
from database import *
app = Flask(__name__)

# Function to fetch outdoor temperature from Météo-France
def fetch_outdoor_temperature():
    # Get the current time
    current_hour = datetime.now().hour

    # Check if the current hour is one of the hours when data is published (every 3 hours from midnight)
    if current_hour % 3 == 0:
        # Format the date in the required format (YYYYMMDDHH)
        formatted_csv_date = datetime.now().strftime("%Y%m%d%H")
    else:
        # If the current hour is not one of the publishing hours, fetch the data from the last published hour
        formatted_csv_date = (datetime.now() - timedelta(hours=current_hour % 3)).strftime("%Y%m%d%H")
    
    # Construct the URL
    url = f"https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/synop.{formatted_csv_date}.csv"

    # Make the HTTP GET request
    response = requests.get(url)
    
    # Check if request was successful
    try:
        # Decode the content as UTF-8 and split into lines
        lines = response.content.decode('utf-8').splitlines()
        # Read the CSV data using csv.DictReader
        reader = csv.DictReader(lines, delimiter=";")
        
        # Extract outdoor temperature from the CSV data
        for row in reader:
            if row['numer_sta'] == '07149':  
                outdoor_temp = float(row['t'])
                return round(outdoor_temp - 273.15, 1)  # Convert °K to °C
    except Exception as e:
        print(f"[{datetime.now()}] MeteoFrance - Failed to fetch data from Météo-France. Error: {e}")






# Route to display the database contents
@app.route('/')
def dashboard():
    data = fetch_all_data()[:5]

    # Convert figure to JSON for rendering in template
    temp_graph_json = history_graph_temp()
    HR_graph_json = history_graph_HR()
    outdoor_temp = fetch_outdoor_temperature()

    return render_template('index.html', data=data, temperature=outdoor_temp,  temp_graph_json=temp_graph_json, HR_graph_json=HR_graph_json)

#Route to display the sensor history
@app.route('/history')
def history():
    data = fetch_all_sensor()
    disp_data = []
    sensors_name = []
    for mac, name in data:
        disp_data += [fetch_data_by_sensor(name)]
        sensors_name.append(name)


    
    return render_template('history.html', S1=disp_data[0], S2=disp_data[1], S3=disp_data[2], sensor=sensors_name)

@app.route('/adm', methods=['GET'])
def admin():
            

    # Fetch sensor data
    data = fetch_all_sensor()

    # Fetch email settings
    email_settings = fetch_email_settings()

    #Fetch threshold settings
    threshold_settings = fetch_threshold_settings()
    return render_template('admin.html', data=data, sensors=data, email_settings=email_settings, threshold_settings=threshold_settings)

@app.route('/updateMail', methods=['POST'])
def update_mail():
    # Process the form data here
    smtp_id = request.form['smtp_id']
    smtp_pwd = request.form['smtp_pwd']
    smtp_server = request.form['smtp_server']
    smtp_port = request.form['smtp_port']
    recipient_email = request.form['recipient_email']
    max_hr = request.form['MAX_HR']
    max_temp = request.form['MAX_TEMP']
    
    # Update email settings in the database
    update_email_settings(smtp_id, smtp_pwd, smtp_server, smtp_port, recipient_email)
    # Update threshold settings in the database
    update_threshold_settings(max_hr, max_temp)

    # Redirect to a success page or render a template
    return redirect("/adm")

@app.route('/updateSensor', methods=['POST'])
def updateSensor():
    # Get sensor name form data
    old_name = request.form['old_name']
    new_name = request.form['new_name']

    update_sensor_settings(new_name, old_name)

    return redirect("/adm")

def run_flask():
    app.run()

def RunInThread_WebServer():
    threading.Thread(target=run_flask, daemon=True).start()
if __name__ == '__main__':
    print(fetch_outdoor_temperature)

