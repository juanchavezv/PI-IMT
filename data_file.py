from serial.tools import list_ports
import serial
import time
import csv

f = open("data.csv","w",newline='')
f.truncate

serialCom = serial.Serial('COM7',9600)

kmax = 5 #maximo numero de datos a leer
for k in range(kmax):
    try:
        s_bytes = serialCom.readline()
        decoded_bytes = s_bytes.decode("utf-8").srtip('\r\n')
        print(decoded_bytes)
    except:
        print('Error')
