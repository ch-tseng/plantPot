# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import sys, time
from datetime import datetime
import serial
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plot
from classPlantPot.lamp import light
from classPlantPot.pump import water

Serial = serial.Serial("/dev/ttyS0", 9600, timeout= 0.5 )

light1 = light(Serial, threshold=900, periodTime=(6,17), historyKeep=120)
light1.valueNow = 0
light1.powerNow = 0

water1 = water(Serial, threshold=300, periodTime=(6,17), historyKeep=120)
water1.valueNow = 0
water1.powerNow = 0

nowTemperature = 0
nowHumandity = 0

def readSerial():
    global light1, nowTemperature, nowHumandity
    recv = ""
    dataString = ""
    count = int(Serial.inWaiting())

    if count > 0:
        recv = Serial.read(count).decode('utf-8')

        aLoc = recv.find("[")
        bLoc = recv.find("]")

        if(aLoc>=0 and bLoc>0 and aLoc<bLoc):
            dataString = recv[aLoc+1:bLoc]
            dataList = dataString.split(",")

            for dataValue in dataList:
                sType, sValue, sPower = dataValue.split(":")
                sPower = int(sPower)

                if(sType=="T"):
                    nowTemperature = float(sValue)
                elif(sType=="H"):
                    nowHumandity = float(sValue)
                elif(sType=="L"):
                    light1.valueNow = int(sValue)
                    light1.powerNow = sPower
                elif(sType=="W"):
                    water1.valueNow = int(sValue)
                    water1.powerNow = sPower


while True:
    readSerial()
    print ("Light:", light1.valueNow, light1.powerNow)
    print ("Water:", water1.valueNow, water1.powerNow)
    print ("T, H:", nowTemperature, nowHumandity)

    try:
        light1.putSensorData(light1.valueNow, light1.powerNow)
        water1.putSensorData(water1.valueNow, water1.powerNow)
    except:
        print("Error occurred: light1.putSensorData({}.{})".format(light1.valueNow, light1.powerNow))
        pass

    time.sleep(1)
