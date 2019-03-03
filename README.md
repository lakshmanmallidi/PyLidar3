# PyLidar3

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/lakshmanmallidi/PyLidar3) [![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/lakshmanmallidi/PyLidar3/License)
<br />PyLidar3 is python 3 package to get data from Lidar device. Currently supports ydlidar from [www.ydlidar.com/]([www.ydlidar.com/).

## Source code
Source code is available on github's repository. <br />
[https://github.com/lakshmanmallidi/PyLidar3/blob/master/PyLidar3/\__init.py\_\_](https://github.com/lakshmanmallidi/PyLidar3/blob/master/PyLidar3/__init__.py)

## Dependencies
* pyserial
* time
* math

## Installation

##### Using Pip
```
pip install PyLidar3
```
You can also install using setup.py file from git repository.

## Usage
This package consists of multiple classes representing the version of lidar you are using. The class structure is YdLidarX4 where X4 is version name ydlidar. 0.1 version of this package does only contain class for X4 version only. Further contribution are actively accepted. 
##### Functions:
YdLidarX4
* `Connect` -- Begin serial connection with Lidar by opening serial port. Return success status True/False.<br />
* `StartScanning` -- Begin the lidar and returns a generator which returns a dictionary consisting angle(degrees) and distance(meters).<br />
 Return Format : {angle(1):distance, angle(2):distance,....................,angle(360):distance}<br />
 Return False in case of exception.<br />
* `StopScanning` -- Stops scanning but keeps serial connection alive.<br />
 Return True on success.<br />
 Return False in case of exception.<br />
* `GetHealthStatus` -- Returns Health status of lidar<br />
 True: good <br />
 False: Not good or Exception or not connected <br />
* `GetDeviceInfo` -- Reboots the Lidar. Return True on success. Return False in case of exception. <br />
* `Reset` -- Reboot the lidar <br />
* `Disconnect` -- Stop scanning and close serial communication with Lidar. <br />
 Return True on success.<br />
 Return False in case of exception.<br />
##### Examples
This Example prints data from lidar
```
import PyLidar3
import time # Time module
#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty* 
port = input("Enter port name which lidar is connected:") #windows
#port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port)
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 30: #scan for 30 seconds
        print(next(gen))
        time.sleep(0.5)
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
```
This Example plot the data. This example needs matplotlib library.
```
import threading
import PyLidar3
import matplotlib.pyplot as plt
import math    
import time

def draw():
    global is_plot
    while is_plot:
        plt.figure(1)
        plt.cla()
        plt.ylim(-9000,9000)
        plt.xlim(-9000,9000)
        plt.scatter(x,y,c='r',s=8)
        plt.pause(0.001)
    plt.close("all")
    
                
is_plot = True
x=[]
y=[]
for _ in range(361):
    x.append(0)
    y.append(0)

port =  input("Enter port name which lidar is connected:") #windows
Obj = PyLidar3.YdLidarX4(port)
threading.Thread(target=draw).start()
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 30: #scan for 30 seconds
        data = next(gen)
        for angle in range(0,361):
            if(data[angle]>1000):
                x[angle] = data[angle] * math.cos(math.radians(angle))
                y[angle] = data[angle] * math.sin(math.radians(angle))
    is_plot = False
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")

```
## Testing

A "tesing" branch is maintained in the git repository for testing, debugging and updating the code. Please visit Github repo [https://github.com/lakshmanmallidi/PyLidar3](https://github.com/lakshmanmallidi/PyLidar3) for further information. 
