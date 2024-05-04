from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
import threading
import schedule
from env import *
from database import fetch_email_settings

MESSAGE_TEMP = """

Hi {recipient},

The temperature of {Sensor} as reached {Val} °c at {TimeStamp}.

"""
MESSAGE_HR = """

Hi {recipient},

The HR of {Sensor} as reached {Val} percent at {TimeStamp}.

"""

def email(recipient_email, message, ReachedVal, Sensor, TimeStamp):

    """
    Sends emails with the following arguments:
        - Recipient's email address
        - Message body
        - Reached value either for temp or HR
        - The sensor on wich the values are maxed out
        - the time stamp
    """
    #print(fetch_email_settings())
    sender_email, password, smtp_server, port, recipient_email = fetch_email_settings()

    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"One alert on {Sensor}"  # Update with your email subject

    # Add message body
    body = message.format(recipient=recipient_email, Sensor=Sensor, Val=ReachedVal, TimeStamp=TimeStamp)
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Start a TLS encrypted connection
        server = smtplib.SMTP(smtp_server, int(port))
        server.starttls()

        # Login to the SMTP server
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"[{datetime.now()}] Mail Alerte System - Email sent successfully!")
        # Close the connection
        server.quit()
    except Exception as e:
        print(f"[{datetime.now()}] Mail Alerte System - Failed to send email. Error: {e}")
    finally:
        None


def check_and_send_email():
    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    # Retrieve the last record from SensorData table
    c.execute("SELECT * FROM SensorData ORDER BY Id DESC LIMIT 1")
    last_record = c.fetchone()
    # Retrieve the threshold settings from Alert_settings table    
    c.execute("SELECT MAX_HR, MAX_TEMP FROM alert_settings")
    threshold = c.fetchone()
    print(threshold)

    if last_record:
        # Extract HR and Temp values from the last record
        _, sensor, time, temp, hr, _ = last_record

        # Check if HR or Temp exceed set values
        if temp > threshold[1]:
            email(RECIPIENT, MESSAGE_TEMP, temp, sensor, time)
        if hr > threshold[0]:
            email(RECIPIENT, MESSAGE_HR, hr, sensor, time)
        
    else:
        print(f"[{datetime.now()}] Mail - No data found in the database.")

    # Close database connection
    conn.close()

def RunInThread_MailAlerts():
    now = datetime.now()
    print(f"######################################################################\n[{now}] Open Thread mail check Alert")
    threading.Thread(target=check_and_send_email, daemon=True).start()

def ScheduleMailAlerts():
    schedule.every(2).minutes.do(RunInThread_MailAlerts) #run every 2 minutes