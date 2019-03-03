import serial
import time
import math
name = "YdLidar"
class YdLidarX4:
    """Deals with X4 version of Ydlidar from http://www.ydlidar.com/"""
    def __init__(self,port):
        """Initialize the connection and set port and baudrate."""
        self.__port = port
        self.__baudrate = 128000
        self.__is_scanning = False
        self.__is_connected = False
    def Connect(self):
        """Begin serial connection with Lidar by opening serial port.\nReturn success status True/False.\n"""
        try:
            if(not self.__is_connected):
                self.__s=serial.Serial(self.__port, self.__baudrate)
                self.__is_connected = True
                self.__stop_motor()
                time.sleep(0.5)
                information = self.__s.read_all()
                if(self.GetHealthStatus()):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False
        
    def __start_motor(self):
        if(self.__is_connected):
            self.__s.setDTR(1)
            time.sleep(0.5)
            return True
        else:
            return False
        
    def __stop_motor(self):
        if(self.__is_connected and (not self.__is_scanning)):
            self.__s.setDTR(0)
            time.sleep(0.5)
            return True
        else:
            return False
    @classmethod    
    def __AngleCorr(cls,dist):
        if dist==0:
            return 0
        else:
            return math.atan(21.8*((155.3-dist)/(155.3*dist)))
    @classmethod  
    def __addhex(cls,h,l):
        return h+(l*0x100)
    @classmethod
    def __calculate(cls,d):
        ddict=[]
        LSN=d[1]
        Angle_fsa = ((YdLidarX4.__addhex(d[2],d[3])>>1)/64.0)+YdLidarX4.__AngleCorr(YdLidarX4.__addhex(d[8],d[9]))
        Angle_lsa = ((YdLidarX4.__addhex(d[4],d[5])>>1)/64.0)+YdLidarX4.__AngleCorr(YdLidarX4.__addhex(d[LSN+6],d[LSN+7]))
        if Angle_fsa<Angle_lsa:
            Angle_diff = Angle_lsa-Angle_fsa
        else:
            Angle_diff = 360+Angle_lsa-Angle_fsa
        for i in range(0,2*LSN,2):
            dist_i = YdLidarX4.__addhex(d[8+i],d[8+i+1])
            Angle_i_tmp = ((Angle_diff/float(LSN))*(i/2))+Angle_fsa+YdLidarX4.__AngleCorr(dist_i)
            if Angle_i_tmp > 360:
                Angle_i = Angle_i_tmp-360
            elif Angle_i_tmp < 0:
                Angle_i = Angle_i_tmp+360
            else:
                Angle_i = Angle_i_tmp
            ddict.append((dist_i,Angle_i))
        return ddict
    @classmethod
    def __checksum(cls,data):
        try:
            ocs = YdLidarX4.__addhex(data[6],data[7])
            LSN = data[1]
            cs = 0x55AA^YdLidarX4.__addhex(data[0],data[1])^YdLidarX4.__addhex(data[2],data[3])^YdLidarX4.__addhex(data[4],data[5])
            for i in range(0,2*LSN,2):
                cs = cs^YdLidarX4.__addhex(data[8+i],data[8+i+1]) 
            if(cs==ocs):
                return True
            else:
                return False
        except Exception as e:
            return False
        
    def StartScanning(self):
        """Begin the lidar and returns a generator which returns a dictionary consisting angle(degrees) and distance(meters).\nReturn Format : {angle(1):distance, angle(2):distance,....................,angle(360):distance}\nReturn False in case of exception."""
        try:
            if(self.__is_connected and (not self.__is_scanning)):
                self.__is_scanning = True
                self.__s.reset_input_buffer()
                self.__start_motor()
                self.__s.write(b'\xA5\x60')
                time.sleep(0.5)
                self.__s.read(7)
                while self.__is_scanning == True:
                    data = self.__s.read(1024).split(b"\xaa\x55")[1:-1]
                    distdict = {}
                    countdict = {}
                    for i in range(0,361):
                        distdict.update({i:0})
                        countdict.update({i:0})
                    for e in data:
                        if(e[0]==0):
                            if(YdLidarX4.__checksum(e)):
                                d = YdLidarX4.__calculate(e)
                                for ele in d:
                                    angle = int(round(ele[1]))
                                    prev = distdict[angle]
                                    countdict.update({angle:(countdict[angle]+1)})
                                    curr = prev+((ele[0]-prev)/float(countdict[angle]))
                                    distdict.update({angle:curr})
                    for i in distdict.keys():
                        distdict[i]=int(round(distdict[i]))
                    yield distdict
            else:
                yield False
        except Exception as e:
            yield False
            
    def StopScanning(self):
        """Stops scanning but keeps serial connection alive.\nReturn True on success\nReturn False in case of exception."""
        try:
            if(self.__is_connected and self.__is_scanning):
                self.__is_scanning = False
                self.__s.write(b'\xA5\x65')
                time.sleep(0.5)
                self.__s.reset_input_buffer()
                self.__stop_motor()
                return True
            else:
                return False
        except Exception as e:
            return False

    def GetHealthStatus(self):
        """Returns Health status of lidar\nTrue: good\nFalse: Not good or Exception or not connected\n"""
        try:
            if(self.__is_connected):
                if self.__is_scanning == True:
                    self.StopScanning()
                self.__s.write(b'\xA5\x91')
                time.sleep(0.5)
                data = self.__s.read(10)
                if data[9]==0 and data[8]==0 and (data[7]==0 or data[7]==1):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False
        
    def GetDeviceInfo(self):
        """Return device information of lidar in form of dictonary\n{"model_number":model_number,"firmware_version":firmware_version,"hardware_version":hardware_version,"serial_number":serial_number}\nReturn "False" Not good or Exception or not connected"""
        try:
            if(self.__is_connected):
                if self.__is_scanning == True:
                    self.StopScanning()
                self.__s.write(b'\xA5\x90')
                time.sleep(0.5)
                data = self.__s.read(27)
                model_number = str(data[7])
                firmware_version = str(data[9])+"."+str(data[8])
                hardware_version = str(data[10])
                serial_number = ""
                for i in range(11,20):
                    serial_number = serial_number+str(data[i])
                return {"model_number":model_number,"firmware_version":firmware_version,"hardware_version":hardware_version,"serial_number":serial_number}
            else:
                return False
        except Exception as e:
            return False
        
    def Reset(self):
        """Reboots the Lidar.\nReturn True on success.\nReturn False in case of exception."""
        try:
            if(self.__is_connected):
                self.__s.write(b'\xA5\x40')
                time.sleep(0.5)
                self.Disconnect()
                self.Connect()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    def Disconnect(self):
        """Stop scanning and close serial communication with Lidar."""
        try:
            if(self.__is_connected):
                self.__s.close()
                self.__is_connected=False
                return True
            else:
                return False
        except Exception as e:
            return False
