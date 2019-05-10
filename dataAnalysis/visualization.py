import pyodbc
import matplotlib.pyplot as plt
import numpy as np

conn = pyodbc.connect(r'Driver={SQL Server};Server=localhost;database=LidarData;Trusted_Connection=yes;')
cursor=conn.cursor()

cursor.execute("SELECT TOP 1 * FROM chunk_size_1024")
d_1024 = cursor.fetchall()
cursor.commit()

cursor.execute("SELECT TOP 1 * FROM chunk_size_10240")
d_10240 = cursor.fetchall()
cursor.commit()

cursor.execute("SELECT TOP 1 * FROM original_data")
orgnl_d = cursor.fetchall()[0][:-1]
cursor.commit()

conn.close()

fft_d_1024_1 =np.absolute(np.fft.fft(d_1024[0]))
fft_d_10240_1 =np.absolute(np.fft.fft(d_10240[0]))
fft_orgnl_d=np.absolute(np.fft.fft(orgnl_d))

plt.figure(1)
#plt.plot(d_16000[0],color="red")
plt.plot(d_10240[0],color="blue")
plt.plot(orgnl_d,color="green")

#plt.plot(fft_d_16000_1,color="red")
#plt.plot(fft_d_1024_1,color="blue")
#plt.plot(fft_orgnl_d,color="green")
plt.show()
