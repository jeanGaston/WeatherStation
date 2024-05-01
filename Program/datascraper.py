import schedule
import threading
import time
from env import *
from database import add_sensor_data, fetch_all_sensor
from bluepy.btle import Scanner

def BltDataScrap():
    sensor_dict = {mac: name for mac, name in fetch_all_sensor()}
    scanner = Scanner()
    #print("Begin device scan")
    devices = scanner.scan(timeout=3.0)
    for device in devices:
        if device.addr in SENSORS :
            #print(
            #f"Device found {device.addr} ({device.addrType}), "
            #f"RSSI={device.rssi} dB"
            #)
            for adtype, description, value in device.getScanData():
                if adtype == 22:
                    temp = int(value[24:28], 16) / 100
                    HR = int(value[28:32], 16) / 100
                    Bat = int(value[20:22], 16)
                    #print(f"Temp : {temp} °c \n HR : {HR} % , \n Batterie : {Bat} %")
                    add_sensor_data(DBFILE, sensor_dict[device.addr], time.strftime("%Y-%m-%d %H:%M:%S"), temp, HR, Bat)
                    if temp > MAX_TEMP :
                        
                        email(RECIPIENT, MESSAGE_Temp, temp, sensor_dict[device.addr], time.strftime("%Y-%m-%d %H:%M:%S") )
                        print("mail sent for temp max")
                    elif temp > MAX_HR :
                        email(RECIPIENT, MESSAGE_HR, HR, sensor_dict[device.addr], time.strftime("%Y-%m-%d %H:%M:%S") )
                        print("mail sent for HR max")

                    
    return 0
def RunInThread_DataScrap():
    print("######################################################################\nOpen Thread datascrap")
    threading.Thread(target=BltDataScrap, daemon=True).start()

def ScheduleDataScrap():
    RunInThread_DataScrap()
    schedule.every(10).seconds.do(RunInThread_DataScrap) #run every 10 seconds


