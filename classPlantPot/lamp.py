# -*- coding: utf-8 -*-

'''
power on the light: Serial.write("a".encode())
pwoer off the light: Serial.write("b".encode())

'''

import sys, time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plot


class light():
    def __init__(self, objSerial, threshold=900, periodTime=(6,17) , historyKeep=60):
        self.debug = 1
        self.cmdSerial = objSerial
        self.threshold = threshold
        self.worktime = periodTime
        self.valueList = []
        self.powerValues = []
        self.timeList = []
        self.history = historyKeep

    def power(self, onoff = 0):
        cmdSerial = self.cmdSerial
        if(onoff==1):
            cmdSerial.write("a".encode())
        elif(onoff==0):
            cmdSerial.write("b".encode())

        if(self.debug==1):
            print("debug: power light to ", onoff)

    def putSensorData(self, value, powerStatus):
        time_period = self.worktime
        now = datetime.now()
        dataTime = now.strftime("%H:%M:%S")
        hourNow = int(now.strftime("%H"))

        listValues = self.valueList
        listTimes = self.timeList
        listPowers = self.powerValues

        if(value>0):
            #if the numer of history is over, then remove the oldest one.
            if(len(listValues)>self.history):
                listValues.pop(0)
                listTimes.pop(0)
                listPowers.pop(0)

            threshold = self.threshold

            listValues.append(value)
            listTimes.append(dataTime)
            listPowers.append(powerStatus)

            #the power status of light now
            tmpPower = powerStatus
            #check to see if we are in working time
            if(hourNow<time_period[1] and hourNow>=time_period[0]):
                if(value < threshold):
                    #if the power of light is off now
                    if(powerStatus==0):
                        #power on the light
                        tmpPower = 1

                else:
                    #if the power of the light is on now
                    if(powerStatus==1):
                        #power off the light
                        tmpPower = 0

            else:
                if(powerStatus==1):
                    #power off the light
                    tmpPower = 0

            if(powerStatus != tmpPower):
                self.power(tmpPower)

    def drawLine(self, xlim=None, ylim=None, delta=0.025):

        x1, y1 = self.valueList, self.timeList
        x2, y2 = self.powerValues, self.timeList

        fig, ax = plot.subplots( nrows=1, ncols=1 )  # create figure & 1 axis

        if(xlim is not None):
            ax.set_xlim(self.xlim[0], self.xlim[1])

        if(ylim is not None):
            ax.set_ylim(self.ylim[0], self.ylim[1])

        ax.cla()
        ax.set_title("Lightness (degree)")
        ax.axes.get_xaxis().set_visible(False)

        ax.plot(x1, y1, x2, y2, marker='o')
        fig.canvas.draw()
        # convert canvas to image
        img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        img  = img.reshape(figure.canvas.get_width_height()[::-1] + (3,))
        # img is rgb, convert to opencv's default bgr
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        return img
