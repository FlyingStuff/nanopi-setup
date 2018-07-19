#!/usr/bin/python3

import sht31

import sys
import time


assert(sys.version_info[0] == 3)

def read_temperature_humidity(sensor):
    return sensor.get_temp_and_humidity()

def print_header():
    print("Time, Sensor_Humidity_Outside, Sensor_Temperature_Outside, Sensor_Humidity_Inside, Sensor_Temperature_Inside")


print_header()

while 1:
    sht31_s1 = sht31.SHT31(sys.argv[1], 0x44)
    temp_s1, humidity_s1 = read_temperature_humidity(sht31_s1)
    sht31_s1.close()

    sht31_s2 = sht31.SHT31(sys.argv[1], 0x45)
    temp_s2, humidity_s2 = read_temperature_humidity(sht31_s2)
    sht31_s1.close()

    time.sleep(1)
    print ("%s, %s, %s, %s, %s" % (time.time(), humidity_s1, temp_s1, humidity_s2, temp_s2))


