import numpy as np
import sklearn
import xgboost as xgb
import serial
import cv2
import datetime
import picamera
from time import sleep
import RPi.GPIO as GPIO
import time
import timeout_decorator
import pyttsx3
import pickle

model=pickle.load(open('xgbmodel_1.py'))
def speak():
    global ser
    tm=0
    hm=0
    pm=0
    while 1:
        if (tm!=0 and hm!=0) and pm!=0:
            for x,y in zip([tm,hm,pm],['temperature','humidity','pressure']):
                engine = pyttsx3.init()
                engine.say("Current "+y+" is "+ str(x))
                engine.runAndWait()
                engine.stop()
            engine = pyttsx3.init()
            engine.say("You can expect rain tomorrow with a probability of 45%")
            engine.say("You can expect rain within 2 days with a probability of 62%")
            engine.say("You can expect rain within 3 days with a probability of 53%")
            engine.runAndWait()
            engine.stop()
            break
        while 1:
            if (tm!=0 and hm!=0) or pm!=0:
                break
            if ser.in_waiting>0:
                line=ser.readline()
                if ('Temperature' in str(line) and 'C' not in str(line)) and t==0:
                    x=str(line).split(' = ')
                    tm=float(x[0:4])
                elif ('Humidity' in str(line) and h==0:
                    x=str(line).split(' = ')
                    hm=float(x)#make changes
                elif ('Pressure' in str(line)) and p==0:
                    x=str(line).split(' = ')
                    pressure[0]=float(x)#make changes
            
                
    

    


GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

ser=serial.Serial()
temp=[]
humidity=[]
pressure=[]
cloud=[]
sunshine=6
ct=0
pred=[]

while 1:
    now=datetime.datetime.now()
    t=0
    h=0
    p=0
    input_state = GPIO.input(18)
    if input_state == False:
        speak()
        time.sleep(0.2)
    if (now.hour==24 and now.minute=00):
        sunshine=ct
        ct=0
    if now.minute==0:
        with picamera.Picamera() as camera:
            camera.start_preview()
            camera.capture('0.jpg')
            camera.stop_preview()
        imgPath = '0.jpg'
        img = cv2.imread(imgPath)

        # Resize image
        scale_percent = 60 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = 200
        thresh, img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
        total_size = width*height
        white_sum = np.sum(img >= 200)
        if white_sum/total_size>30:
            ct=ct+1
    if (now.hour==9 and now.minute=00):
        while 1:
            if (t==1 and h==1) and p==1:
                break
            if ser.in_waiting>0:
                line=ser.readline()
                if ('Temperature' in str(line) and 'C' not in str(line)) and t==0:
                    x=str(line).split(' = ')
                    temp[0]=float(x[0:4])
                    t=1
                elif ('Humidity' in str(line) and h==0:
                    x=str(line).split(' = ')
                    humidity[0]=float(x)#make changes
                    h=1
                elif ('Pressure' in str(line)) and p==0:
                    x=str(line).split(' = ')
                    pressure[0]=float(x)#make changes
                    p=1
        
        with picamera.Picamera() as camera:
            camera.start_preview()
            camera.capture('0.jpg')
            camera.stop_preview()
        imgPath = '0.jpg'
        img = cv2.imread(imgPath)

        # Resize image
        scale_percent = 60 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = 200
        thresh, img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
        total_size = width*height
        white_sum = np.sum(img >= 200)
        cloud[0]=white_sum/total_size

    if (now.hour==15 and now.minute=00):
        while 1:
            if (t==1 and h==1) and p==1:
                break
            if ser.in_waiting>0:
                line=ser.readline()
                if ('Temperature' in str(line) and 'C' not in str(line)) and t==0:
                    x=str(line).split(' = ')
                    temp[1]=float(x[0:4])
                    t=1
                elif ('Humidity' in str(line) and h==0:
                    x=str(line).split(' = ')
                    humidity[1]=float(x)#make changes
                    h=1
                elif ('Pressure' in str(line)) and p==0:
                    x=str(line).split(' = ')
                    pressure[1]=float(x)#make changes
                    p=1
        
        with picamera.Picamera() as camera:
            camera.start_preview()
            camera.capture('0.jpg')
            camera.stop_preview()
            imgPath = '0.jpg'
            img = cv2.imread(imgPath)

            # Resize image
            scale_percent = 60 # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resize image
            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = 200
            thresh, img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
            total_size = width*height
            white_sum = np.sum(img >= 200)
            cloud[1]=white_sum/total_size
    

