#!/usr/bin/python
import datetime
import json
import time
import requests
import csv
import math
# Uppsetning á seven segment skjá:
# code modified, tweaked and tailored from code by bertwert
# on RPi forum thread topic 91796
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO ports for the 7seg pins
segments =  (11,4,23,8,7,10,18,25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# GPIO ports for the digit 0-3 pins
digits = (22,27,17,24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}
# Búið að setja upp seven segment skjá
# pip install requests
# C:\Users\Sigurduroo\Desktop\py>python landsnet_data.py

LANDSNET_DATA = None
def save_to_json(filepath, data, pretty=False):
    '''
    takes in filepath and data object saves data to json in filepath
    '''
    if pretty:
        data_text = json.dumps(data, indent=4, ensure_ascii=False,
sort_keys=True)
    else:
        data_text = json.dumps(data, separators=(',', ':'),
ensure_ascii=False, sort_keys=True)
    with open(filepath, mode='w', encoding='utf-8') as json_file:
        json_file.write(data_text)
def fetch_landsnet_data():
    time.sleep(1)
    landsnet_page =
'https://www.landsnet.is/flutningskerfid/kerfisstjornun/aflflutningur-nuna/'
    url = 'https://amper.landsnet.is/MapData/api/measurements'
    res = requests.get(url)
    data = res.json()
    better_data = {}
    for measurement in data:
        better_data[measurement['key']] = measurement
    save_to_json('better_data.json', better_data, pretty=True)

    gogn1 = (better_data['TA1']['MW']) # velja gögn til að birtal
    gogn2 = (better_data['TA1']['time'])

    print("hallo heimur")
    print(gogn1)
    print(gogn2)

        # Stærðargráða tölunnar fundin (hvar komman er)
    if gogn1 == 0:
        staerdargrada_gogn1 = 0
    else:
        staerdargrada_gogn1 = int(math.floor(math.log10(abs(gogn1))))
    if gogn1 < 0:
        gogn1_formatted == gogn1
    else:
        gogn1_formatted = gogn1/pow(10,staerdargrada_gogn1)*1000 #
Talan sett á staðlað form
    # Seven segment keyrsla:

    try:
        while True:
        #    n = time.ctime()[11:13]+time.ctime()[14:16]
        #    s = str(n).rjust(4)
            # a = int(gogn3*1000)
            if gogn1_formatted == 0:
                a = 0
            else:
                a = int(gogn1_formatted)

            #  print(a)
            s = str(a)  # Hér seturðu inn töluna sem þú vilt birta.

            if staerdargrada_gogn1 > 3:  # Ef talan er stærri en 9999
þá birtist 9999 á skjánum
                s = '9999'
            elif staerdargrada_gogn1 == -1: # Ef talan er núll komma
eitthvað þá bætist 0 framan á strenginn
                s = '0' + s
            elif staerdargrada_gogn1 == -2: # Ef talan byrjar á 0.0
bætist 00 framan á strenginn
                s = '0' + '0' + s
            elif staerdargrada_gogn1 == -3: # Ef talan byrjar á 0.00
bætist 000 framan á strenginn
                s = '0' + '0' + '0' + s
            elif staerdargrada_gogn1 < -3: # Ef talan byrjar á 0.000
þá birtist 0000 á skjánum
                s = '0000'
            for digit in range(4):
                for loop in range(0,7):
                    GPIO.output(segments[loop], num[s[digit]][loop])
# Hér kemur á dislpaly
                    #if (int(time.ctime()[18:19])%2 == 0) and (digit
== 1): # Hér er staðeing puntins.gp
                    #    GPIO.output(25, 1)
                    #else:
                    #    GPIO.output(25, 0)
                    if -3 <= staerdargrada_gogn1 < 1 and digit == 0: #
Staðsetning punkts fyrir litla tölu
                        GPIO.output(25,1)
                    elif staerdargrada_gogn1 == 1 and digit == 1: #
Staðsetning punkts fyrir tugatölu
                        GPIO.output(25,1)
                    elif staerdargrada_gogn1 == 2 and digit == 2: #
Staðsetning punkts fyrir hundruð
                        GPIO.output(25,1)
                GPIO.output(digits[digit], 0)
                time.sleep(0.001) # Skiptir á milli dig hraðin
                GPIO.output(digits[digit], 1)
                GPIO.output(25,0)

    finally:

        GPIO.cleanup()
# kÓÐIN FYRIR NEÐAN ER AÐ HANN ENDURHLEÐUR EFTIR 50000000000sek
def main():
    data_timestamp = time.time_ns()
    data = fetch_landsnet_data()
    temp = None
    while True:
        current_timestamp = time.time_ns()
        data_age = current_timestamp - data_timestamp
        if (data_age > 400000):  # nanoseconds
            print('reloading data')
            data_timestamp = time.time_ns()
            data = fetch_landsnet_data()

if __name__ == '__main__':
    main()
