import RPi.GPIO as GPIO
import time
import json
import requests

#GPIO SETUP
moisture_channel = 7
irrigation_channel = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture_channel, GPIO.IN)
GPIO.setup(irrigation_channel, GPIO.OUT)

#Global variables
hardware_id = "001"
moisture_state = ""
valve_status = ""

def postIrrigation(valve_status):
    data ={"hardware_id": hardware_id, "valve_status": valve_status}
    url = "http://ec2-18-207-209-137.compute-1.amazonaws.com:8000/dashboard/addirrigation/"
    header = {'Content-Type':'application/json'}
    response = requests.post(url, json=data,headers=header)
    print("Post Irrigation response:")
    print(response)
    
def postMoisture(moisture_state):
    data ={"hardware_id": hardware_id, "moisture_state": moisture_state}
    url = "http://ec2-18-207-209-137.compute-1.amazonaws.com:8000/dashboard/addmoisture/"
    header = {'Content-Type':'application/json'}
    response = requests.post(url, json=data,headers=header)
    print("Post Moisture response:")
    print(response)
    
def readmoisture():
    
    if GPIO.input(moisture_channel):
        GPIO.output(irrigation_channel, GPIO.HIGH)
        print ("NO Water Detected!")
        moisture_state = "Dry"
        valve_status = "Open"
        time.sleep(1)
        postMoisture(moisture_state)
        postIrrigation(valve_status)
        
    else:
        GPIO.output(irrigation_channel, GPIO.LOW)
        print ("Water Detected!")
        moisture_state = "Wet"
        valve_status = "Close"
        time.sleep(1)
        postMoisture(moisture_state)
        postIrrigation(valve_status)
    
try:
    while True:
        readmoisture()
        time.sleep(30)
        
finally:
    GPIO.cleanup()
          
 
