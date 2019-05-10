import pyodbc
import pickle
f=open('data.txt','r')
processed_data=[]
line=None
while(line!=""):
    try:
        line=f.readline()
        angle_str,distance_str = line.split(",")
        processed_data.append((int(round(float(angle_str.split(":")[1]))),int(distance_str.split(":")[1])))
    except Exception as e:
        print(e)
original_data = {}
countdict = {}
for angle in range(0,361):
    original_data.update({angle:0})
    countdict.update({angle:0})
for ele in processed_data:
    angle = ele[0]
    prev = original_data[angle]
    countdict.update({angle:(countdict[angle]+1)})
    curr = prev+((ele[1]-prev)/float(countdict[angle]))
    original_data.update({angle:curr})
for angle in original_data.keys():
    original_data[angle]=int(round(original_data[angle]))
f.close()

f=open("data.pkl",'rb')
data = pickle.load(f)
f.close()
f=open("data.txt",'rb')
conn = pyodbc.connect(r'Driver={SQL Server};Server=localhost;Trusted_Connection=yes;')
cursor=conn.cursor()
cursor.execute("select count(*) from sys.databases where name='LidarData'")
if(int(cursor.fetchone()[0])>0):
    cursor.commit()
    cursor.execute("drop database LidarData")
cursor.commit()
cursor.execute('create database LidarData')
cursor.commit()
cursor.execute('use LidarData')
cursor.commit()
for chunk_size in data.keys():
    query="create table chunk_size_{}(".format(chunk_size)
    for angle in data[chunk_size][0][0].keys():
        query=query+"Deg_"+str(angle)+" int not null,"
    query=query+"time_intervel float not null)"
    cursor.execute(query)
    cursor.commit()
for chunk_size in data.keys():
    for elements in data[chunk_size]:
        angle_distance_dict,time_intervel = elements
        query="insert into chunk_size_{}(".format(chunk_size)
        for angle in angle_distance_dict.keys():
            query=query+"Deg_"+str(angle)+","
        query=query+"time_intervel) values("
        for distance in angle_distance_dict.values():
            query=query+str(distance)+","
        query=query+str(time_intervel)+")"
        cursor.execute(query)
    cursor.commit()

query="create table original_data("
for angle in original_data.keys():
    query=query+"Deg_"+str(angle)+" int not null,"
query=query[:-1]+")"
cursor.execute(query)
cursor.commit()
query="insert into original_data("
for angle in original_data.keys():
    query=query+"Deg_"+str(angle)+","
query=query[:-1]+") values("
for distance in original_data.values():
    query=query+str(distance)+","
query=query[:-1]+")"
cursor.execute(query)
cursor.commit()

conn.close()
