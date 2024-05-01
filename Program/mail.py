from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
import threading


import schedule
from env import *

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
    port = SMTP_PORT # For SSL
    smtp_server = SMTP
    sender_email = SMTP_ID  # Enter your address
    password = SMTP_PWD
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
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()

        # Login to the SMTP server
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        # Close the connection
        server.quit()

def check_and_send_email():
    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    # Retrieve the last record from SensorData table
    c.execute("SELECT * FROM SensorData ORDER BY Id DESC LIMIT 1")
    last_record = c.fetchone()

    if last_record:
        # Extract HR and Temp values from the last record
        _, sensor, time, temp, hr, _ = last_record

        # Check if HR or Temp exceed set values
        if temp > MAX_HR:
            email(RECIPIENT, MESSAGE_TEMP, temp, sensor, time)
        elif hr > MAX_TEMP:
            email(RECIPIENT, MESSAGE_HR, temp, sensor, time)

    else:
        print("No data found in the database.")

    # Close database connection
    conn.close()

def RunInThread_MailAlerts():
    now = datetime.now()
    print(f"######################################################################\n[{now}] Open Thread mail check Alert")
    threading.Thread(target=check_and_send_email, daemon=True).start()

def ScheduleMailAlerts():
    schedule.every(2).minutes.do(RunInThread_MailAlerts) #run every 2 minutes