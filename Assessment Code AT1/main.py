#// Authors : Carter Hardiman, Dylan Wilson & Omar Gharib 12/11/20
#// Copyright 2019 Steve Gale - seek permission and terms of use before you copy or modify this code
# https://github.com/micropython/micropython-lib/tree/master/urequests
# https://docs.pycom.io/firmwareapi/micropython/usocket/
# https://forum.pycom.io/topic/4068/json-posts
# modified for version 3 - new table structure


#import appropriate modules
import urequests as requests
import ujson
import time

#import data libraries for pycom sensors
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

#set up sensors
py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

#determine variables for the while loop
counter = 0
IOTSensorLocation = "13180006"
Measurement = "Humidity"

#commence while loop to gather data and print it to the server each second
while counter < 30:
    
    #measure humidity from the si sensor
    MeasuredValue = si.humidity()

    #content to print for the server
    contentStr = '{ "IOTSensorLocation" : "%s", "Measurement" : "%s", "Value": "%.2f" }'%(IOTSensorLocation,Measurement,MeasuredValue)

    # url IP address of AWS instance - 27/10/20 (tested in AWS V3)
    url = "http://54.66.192.25/i40Test/v3/InsertJsonRESTData.php" 


    r = requests.post(url, data = contentStr)       # post request to API with json content data
    print(r.text)                                   # print the json response string
    json_data = r.json()                            # make json object from response
    r.close()                                       # close connection
    print(json_data)
    print("code = {0} : message = {1} ".format(json_data['code'],json_data['message']))     # extract the json data
    print("code = {0} : message = {1} : Meas={2} : Setpoint={3} : Deadband={4}".format(json_data['code'],json_data['message'],json_data['Measurement'],json_data['Setpoint'],json_data['Deadband']))     # extract the json data

    #set count intervals and repeat data upload every second
    counter = counter+1
    time.sleep_us(1000)