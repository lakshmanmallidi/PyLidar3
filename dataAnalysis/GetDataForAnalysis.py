import lidar
import time 
import pickle
chunk_sizes = [3000,4000,6000]
storage = {}
port = input("Enter port name which lidar is connected:") #windows
time.sleep(5)
for size in chunk_sizes:
    Obj = lidar.YdLidarG4(port,size)
    if(Obj.Connect()):
        print(Obj.GetDeviceInfo())
        gen = Obj.StartScanning()
        t = time.time()
        storage.update({size:[]})
        while (time.time() - t) < 30: 
            storage[size].append((next(gen),time.time()-t))
        Obj.StopScanning()
        Obj.Disconnect()
    else:
        print("Error connecting to device")
    time.sleep(5)

f=open("data.pkl",'wb')
pickle.dump(storage,f)
f.close()
