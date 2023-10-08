# sudo apt-get install python 
# sudo apt-get update
# sudo apt-get install rpi.gpio
# sudo apt-get install -y python-requests
# sudo apt-get install python time
# sudo pip install requests
# sudo pip3 install requests
# sudo apt-get upgrade
# python3 (run program)
#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import time
import math
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

receive_pin = 38
GPIO.setup(receive_pin, GPIO.IN)

# GPIO ports for the 7seg pins
segments =  (11, 4, 23, 8, 7, 10, 18, 25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# GPIO ports for the digit 0-3 pins
digits = (22, 27, 17, 24)
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
LANDSNET_DATA = None

def save_to_json(filepath, data, pretty=False):
    if pretty:
        data_text = json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
    else:
        data_text = json.dumps(data, separators=(',', ':'), ensure_ascii=False, sort_keys=True)
    with open(filepath, mode='w', encoding='utf-8') as json_file:
        json_file.write(data_text)

def fetch_landsnet_data():
    landsnet_page = 'ASK AUTHORS!'
    url = 'ASK AUTHORS!'
    res = requests.get(url)
    data = res.json()
    better_data = {}
    for measurement in data:
        better_data[measurement['key']] = measurement
    save_to_json('better_data.json', better_data, pretty=True)
    gogn1 = better_data['TA1']['MW']
    gogn2 = better_data['TA1']['time']
    print("hallo heimur")
    print(gogn1)
    print(gogn2)
    
    if gogn1 == 0:    
        staerdargrada_gogn1 = 0
    else:
        staerdargrada_gogn1 = int(math.floor(math.log10(abs(gogn1))))
    if gogn1 < 0:
        gogn1_formatted = gogn1
    else:
        gogn1_formatted = gogn1 / pow(10, staerdargrada_gogn1) * 1000
    # Seven segment keyrsla:
    try:
        while True:
            if gogn1_formatted == 0:
                a = 0
            else:
                a = int(gogn1_formatted)
            #  print(a)
            s = str(a)
            if staerdargrada_gogn1 > 3:
                s = '9999'
            elif staerdargrada_gogn1 == -1:
                s = '0' + s
            elif staerdargrada_gogn1 == -2:
                s = '0' + '0' + s
            elif staerdargrada_gogn1 == -3:
                s = '0' + '0' + '0' + s
            elif staerdargrada_gogn1 < -3:
                s = '0000'
            for digit in range(4):
                for loop in range(0,7):
                    GPIO.output(segments[loop], num[s[digit]][loop])
                    if -3 <= staerdargrada_gogn1 < 1 and digit == 0:
                        GPIO.output(25,1)
                    elif staerdargrada_gogn1 == 1 and digit == 1:
                        GPIO.output(25,1)
                    elif staerdargrada_gogn1 == 2 and digit == 2:
                        GPIO.output(25,1)
                GPIO.output(digits[digit], 0)
                time.sleep(0.005)
                GPIO.output(digits[digit], 1)
                GPIO.output(25,0)
                if check_voltage():
                       print("Spenna kom á pinna 38! Endurrótum forritið...")
                       time.sleep(0.01)  # Bíða í 100ms
                if check_voltage():
                    return  # Hætta í loopu ef spenna er kominn aftur
                
    finally:
        GPIO.cleanup()

def check_voltage():
    return GPIO.input(receive_pin) == GPIO.HIGH

def main():
    while True:
        fetch_landsnet_data()

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
