'''
Baron IoT 
    - Measures temperature and humidity
    - Detect several solid objects up to 10m away in a wide sensing range, 
    - or use this Phidget as an ultrasonic range finder.


Modified / Upgraded by : @bencarpena

# Change log:
@bencarpena :   20210117    :   Initial setup
                            :   Added self-healing subroutines
            :   20210201    :   Reviewed error trapping; removed `pass`
            :   20210202    :   Added flush buffered data


References:
-   https://www.phidgets.com/education/learn/device-tutorials/humidity-sensor/

'''
#Add Phidgets library
from Phidget22.Phidget import *
from Phidget22.Devices.HumiditySensor import *
from Phidget22.Devices.TemperatureSensor import *
#Required for sleep statement

import os, sys, time

def Activate_Baron():
    #Create
    humiditySensor = HumiditySensor()
    temperatureSensor = TemperatureSensor()

    #Open
    humiditySensor.openWaitForAttachment(1000)
    temperatureSensor.openWaitForAttachment(1000)

    #Use your Phidgets
    while (True):
        print("Humidity: " + str(humiditySensor.getHumidity()) + " %RH")
        print("Temperature: " + str(temperatureSensor.getTemperature()) + "°C\n")
        time.sleep(0.5)



#Open and Code driver
try:
   Activate_Baron()
except:
    print("INFO: Error encountered at Temp & Humidity sensor (HUM1000_0). Healing now...")

    #err = sys.exc_info()[0] ##--> <class 'Phidget22.PhidgetException.PhidgetException'>
    #print (err)

    
    # === self-healing protocol; start from top ===
    #v1: 
    # os.execv(__file__, sys.argv)
    #v2:
    sys.stdout.flush() # flush buffered data
    os.execv(sys.executable, ['python3'] + [sys.argv[0]])

finally:
    pass


  