from serial.tools import list_ports
import serial
import time
import csv

f = open("data.csv","w",newline='')
f.truncate

serialCom = serial.Serial('COM7',9600)
