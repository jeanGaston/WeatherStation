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


while True:
    schedule.run_pending()
    time.sleep(1)

