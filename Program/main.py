from database import *
from datascraper import *
from Webserver import RunInThread_WebServer
from mail import ScheduleMailAlerts
from env import *
import schedule

check_database(DBFILE)
RunInThread_WebServer()
ScheduleDataScrap()
ScheduleMailAlerts()
#print_email_settings()


while True:
    schedule.run_pending()
    time.sleep(1)

