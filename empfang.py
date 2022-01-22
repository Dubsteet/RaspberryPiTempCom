import time, sys, requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#GPIO Plätze der LED
RED_PIN = 17
YELLOW_PIN = 27
GREEN_PIN = 22

#Adresse der REST-API
REQ_URL = '192.168.178.36:8000'

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
 
#Abfrage der Temperatur mit der gegebenen ID
def readTempFromServer(id) :
    req = requests.get('http://' + REQ_URL + '/index.php?id=' + str(id))
    jason = req.json()
    return jason[0]["temp"]

#Abragen der ID von der neusten Abfrage
def readMaxID() :
    req = requests.get('http://' + REQ_URL + '/index.php?totalentrycount=true')
    jason = req.json()
    return jason["totalentrycount"]
try:
    id = -1
    while True :
        newId = readMaxID()
        if (newId > id) :
            id = newId
            temp = readTempFromServer(id)
            print(temp)
            #Je nach Temperatur werden die LED geschaltet
            if (temp < 20) :
                print('GREEN')
                GPIO.output(RED_PIN, GPIO.LOW)
                GPIO.output(YELLOW_PIN, GPIO.LOW)
                GPIO.output(GREEN_PIN, GPIO.HIGH)
            elif (temp < 23) :
                print('YELLOW')
                GPIO.output(RED_PIN, GPIO.LOW)
                GPIO.output(YELLOW_PIN, GPIO.HIGH)
                GPIO.output(GREEN_PIN, GPIO.LOW)
            else :
                print ('RED')
                GPIO.output(RED_PIN, GPIO.HIGH)
                GPIO.output(YELLOW_PIN, GPIO.LOW)
                GPIO.output(GREEN_PIN, GPIO.LOW)
except KeyboardInterrupt:
    # Programm wird beendet wenn STRG+C gedrückt wird.
    print('Temperaturmessung wird beendet')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    print('Programm wird beendet.')
    GPIO.cleanup()
    sys.exit(0)