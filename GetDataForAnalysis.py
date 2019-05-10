import lidar
import time 
import pickle
chunk_sizes = [1024,2048,10240]
storage = {}
port = input("Enter port name which lidar is connected:") #windows
time.sleep(10)
for size in chunk_sizes:
    Obj = lidar.YdLidarG4(port,size)
    if(Obj.Connect()):
        print(Obj.GetDeviceInfo())
        gen = Obj.StartScanning()
        t = time.time()
        storage.update({size:[]})
        while (time.time() - t) < 250: 
            storage[size].append((next(gen),time.time()-t))
        Obj.StopScanning()
        Obj.Disconnect()
    else:
        print("Error connecting to device")
    time.sleep(20)

f=open("data.pkl",'wb')
pickle.dump(storage,f)
f.close()
