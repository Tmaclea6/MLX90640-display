import serial
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import pygame


def connectArduino(port='COM4'):
    '''port - (string) The com port that the Arduino is connected to.\n
       This sets up a connection to the Arduino and checks that it is open. If
       it doesn't open, it stops everything and outputs a message. The port
       varible is the only thing that might need to change. Check your device
       manager to see what port the arduino is using.
    '''
    serArduino = serial.Serial(
        port,
        baudrate=74880,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)

    # Make sure the Arduino port is open (try closing first just in case)
    serArduino.close()
    serArduino.open()
    if not serArduino.isOpen():
        print('ERROR: Could not connect to Arduino')
        sys.exit()
    else:
        # You have to wait an amount of time between when you open port and when
        # you start to use it, otherwise there could be a crash.
        time.sleep(1)
        print('Arduino is connected.')
        return serArduino


heatMap = np.random.random((24, 32))
fig = plt.figure()
ax = fig.add_subplot(111)

plt.show(block=False)
Arduino = connectArduino()
while True:
    line = Arduino.readline()
   # print(line)
    if line == b'frame\r\n':
        for x in range(0, 24):
            for y in range(0, 32):
                data = Arduino.readline()
                heatMap[x][y] = data
    #print(heatMap)
    first = True
    if first:
        im = ax.imshow(heatMap)

   # time.sleep(0.1)
    # replace the image contents
    im.set_array(heatMap)
    # redraw the figure
    fig.canvas.draw()
    fig.canvas.flush_events()
