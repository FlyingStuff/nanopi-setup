#!/usr/bin/python3

import sht31

import sys
import time


assert(sys.version_info[0] == 3)

def read_temperature_humidity(sensor):
    return sensor.get_temp_and_humidity()



while 1:
    sht31_s1 = sht31.SHT31(sys.argv[1], 0x44)
    temp_s1, humidity_s1 = read_temperature_humidity(sht31_s1)
    sht31_s1.close()

    print ("Temperature Sensor 1: %s" % temp_s1)
    print ("Humidity Sensor 1: %s" % humidity_s1)

    time.sleep(1)

sht31_s2 = sht31.SHT31(sys.argv[1], 0x45)
temp_s2, humidity_s2 = read_temperature_humidity(sht31_s2)
# sht31_s2.close()

print ("Temperature Sensor 2: %s" % temp_s2)
print ("Humidity Sensor 2: %s" % humidity_s2)

