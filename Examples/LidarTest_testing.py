import threading
import lidar
import matplotlib.pyplot as plt
import math    
import time

def draw():
    global is_plot
    while is_plot:
        plt.figure(1)
        #plt.cla()
        plt.ylim(-4000,4000)
        plt.xlim(-4000,4000)
        plt.scatter(x,y,c='r',s=0.5)
        plt.pause(0.001)
    plt.close("all")
    
                
is_plot = True
x=[]
y=[]
for _ in range(361):
    x.append(0)
    y.append(0)

port =  input("Enter port name which lidar is connected:") #windows
Obj = lidar.YdLidarG4(port)  #PyLidar3.your_version_of_lidar(port,chunk_size)
threading.Thread(target=draw).start()
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 50: #scan for 30 seconds
        data = next(gen)
        for angle in range(0,360):
            x[angle] = data[angle] * math.cos(math.radians(angle))
            y[angle] = data[angle] * math.sin(math.radians(angle))
    is_plot = False
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")



'''
import lidar
import time # Time module
#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty* 
port = input("Enter port name which lidar is connected:") #windows
#port = "/dev/ttyUSB0" #linux
Obj = lidar.YdLidarG4(port)
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    print(Obj.GetCurrentFrequency())
    Obj.IncreaseCurrentFrequency(lidar.FrequencyStep.oneTenthHertz)
    print(Obj.GetCurrentFrequency())
    Obj.DecreaseCurrentFrequency(lidar.FrequencyStep.oneHertz)
    print(Obj.GetCurrentFrequency())
    print(Obj.GetCurrentRangingFrequency())
    Obj.SwitchRangingFrequency()
    print(Obj.GetCurrentRangingFrequency())
    Obj.DisableLowPowerMode()
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 10: #scan for 30 seconds
        data=next(gen)
        print(data)
        time.sleep(0.5)
    print(Obj.GetCurrentFrequency())
    Obj.IncreaseCurrentFrequency(lidar.FrequencyStep.oneHertz)
    print(Obj.GetCurrentFrequency())
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time
    while (time.time() - t) < 20: #scan for 30 seconds
        data=next(gen)
        print(data)
        time.sleep(0.5)
    Obj.Disconnect()
else:
    print("Error connecting to device")
'''
