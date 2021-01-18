'''
Sonar IoT 
    - Measures distance
    - Detect several solid objects up to 10m away in a wide sensing range, 
    - or use this Phidget as an ultrasonic range finder.


Modified / Upgraded by : @bencarpena

Change log:
# 20210115  :   @bencarpena :   Initial setup
            :                   Added self-healing subroutines; sonar phidget expects initial activity reading 
                                for loop to continue



References:
-   https://www.phidgets.com/education/learn/device-tutorials/sonar-sensor/

'''
import os, sys

#Add Phidgets Library
from Phidget22.Phidget import *
from Phidget22.Devices.DistanceSensor import *
#Required for sleep statement
import time

#Create / Instantiate
distanceSensor = DistanceSensor()

#Define function
def Activate_Sonar():
    distanceSensor.openWaitForAttachment(1500) #orig is 1000 

    #Use Sonar Phidget
    sonar_init0_val = distanceSensor.getDistance()
    print ("Initial sensor value: ", str(sonar_init0_val))

    while (True):
        print("Distance: " + str(distanceSensor.getDistance()) + " mm")
        time.sleep(0.25)

#Open and Code driver
try:
   Activate_Sonar()
except:
    print("INFO: Error encountered at Sonar sensor (DST1200_0). Missing data. Healing now...")
    pass

finally:
    #os.execv(__file__, sys.argv)
    os.execv(sys.executable, ['python3'] + [sys.argv[0]])