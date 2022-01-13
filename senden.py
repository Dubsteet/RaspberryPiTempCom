import time, sys, requests
 
#Pfad des Sensors
sensor = '/sys/bus/w1/devices/28-00000cb54bd0/w1_slave'
#Adresse der REST-API
REQ_URL = '192.168.178.36:8000'
#Raum der Messung
ROOM = 'Zuhause'
 
#Auslesen des Temperatursensors
def readTempSensor(sensorName) :
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Auswerten der Ausgabe vom Sensor
def readTempLines(sensorName) :
    lines = readTempSensor(sensorName)
    #Überprüfung ob Sensor fehler meldet
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')
    #Überprüfung ob Temperatur vorhanden
    if temperaturStr != -1 :
        tempData = lines[1][temperaturStr+2:]
        temp = float(tempData) / 1000.0
        return temp
 
try:
    while True :
        temp = str(readTempLines(sensor))
        print(temp)
        #Post Request auf den Webserver
        r = requests.post('http://' + REQ_URL + '?temp='+ temp +'&room=' + ROOM)
        print(r.status_code, r.reason)
        time.sleep(10)
except KeyboardInterrupt:
    #Programm wird beendet wenn STRG+C gedrückt wird.
    print('Temperaturmessung wird beendet')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    print('Programm wird beendet.')
    sys.exit(0)
