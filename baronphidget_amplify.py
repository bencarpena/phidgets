'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Project name      :   altair Temperature + Humidity sensor
# Description       :   Reads temp and humidity at my local area using Phidgets
                    :   and posts data/readings at Slack 
                    :   and Cloud-based services (IoT Hub + Stream Analytics + Azure SQL DB)
# Change log        :
@bencarpena         :   20210308 : 	initial codes created
               


# References:
-   https://www.phidgets.com/education/learn/device-tutorials/humidity-sensor/

# MQTT personal notes:
https://onedrive.live.com/view.aspx?resid=BE42616FC86F2AB8%2119663&id=documents&wd=target%28IoT.one%7C2C2A8BC3-E1B8-2541-9366-F6F8E984C1BF%2FIntegrating%20MQTT%20and%20Azure%20IoT%20Hub%7CCB2F4618-D393-034D-95F5-04A5DFAE8239%2F%29
onenote:https://d.docs.live.net/be42616fc86f2ab8/Documents/archived/Technical%20Notebook/IoT.one#Integrating%20MQTT%20and%20Azure%20IoT%20Hub&section-id={2C2A8BC3-E1B8-2541-9366-F6F8E984C1BF}&page-id={CB2F4618-D393-034D-95F5-04A5DFAE8239}&end

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

import sys


import ssl, os
import requests
import json

from time import sleep
from datetime import datetime

from paho.mqtt import client as mqtt

from Phidget22.Phidget import *
from Phidget22.Devices.HumiditySensor import *
from Phidget22.Devices.TemperatureSensor import *

#from slack import WebClient 


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
			ssl._create_default_https_context = ssl._create_unverified_context


try:
    #Create
    humiditySensor = HumiditySensor()
    temperatureSensor = TemperatureSensor()

    #Open
    humiditySensor.openWaitForAttachment(1000)
    temperatureSensor.openWaitForAttachment(1000)

    #Use your Phidgets
    print("Humidity: " + str(humiditySensor.getHumidity()) + " %RH")
    print("Temperature: " + str(temperatureSensor.getTemperature()) + "°C\n")
    sleep(1)

    dtstamp = datetime.now()
    slack_msg = {'text' : 'altair (iothub bypass dht) | ' + str(dtstamp) + \
        ' | Temperature : ' + str(temperatureSensor.getTemperature()) \
        + ' °C | Humidity : ' + str(humiditySensor.getHumidity()) + ' %RH'}
    
    webhook_url = 'https://hooks.slack.com/services/<yourwebhook>' 

    #post to Slack
    requests.post(webhook_url, data=json.dumps(slack_msg))
    
    # debug only:
    #print ("Success : Posted data to Slack!")

    slack_msg_mqtt = '{"iot_msg_from" : "altair(iot/w03)", "iot_dt" : "' + str(dtstamp) + '", "iot_rd" : "sensor = Phidget | Temperature = ' + str(temperatureSensor.getTemperature()) + ' C | Humidity = ' + str(humiditySensor.getHumidity()) + ' %RH"}'

    # @bencarpena 20210308 : Send message to IoT Hub via MQTT
    # START : MQTT < #############################
    path_to_root_cert = "/<your path/Baltimore.pem"
    device_id = "<your iot hub deviceid>"
    sas_token = "SharedAccessSignature sr=<your SAS token>"
    iot_hub_name = "<your iot hub name>"


    def on_connect(client, userdata, flags, rc):
        print("altair (mode: iot/w03) connected with result code: " + str(rc))


    def on_disconnect(client, userdata, rc):
        print("altair (mode: iot/w03) disconnected with result code: " + str(rc))


    def on_publish(client, userdata, mid):
        print("altair (mode: iot/w03) sent message!")
        print("JSON payload sent: ", slack_msg_mqtt)


    def on_message(client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)

    def on_log(client, userdata, level, buf):
        print("log: ",buf)


    client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)
    client.on_message=on_message 
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    client.username_pw_set(username=iot_hub_name+".azure-devices.net/" +
                        device_id + "/?api-version=2018-06-30", password=sas_token)

    client.tls_set(ca_certs=path_to_root_cert, certfile=None, keyfile=None,
                cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    client.tls_insecure_set(False)

    client.connect(iot_hub_name+".azure-devices.net", port=8883)

    #start the loop
    client.loop_start() 

    #subscribe to topic
    client.subscribe("devices/" + device_id + "/messages/events/")

    #publish message
    client.publish("devices/" + device_id + "/messages/events/", slack_msg_mqtt, qos=1) 

    #give time to process subroutines
    sleep(5)

    #display log
    client.on_log=on_log


    #end the loop
    client.loop_stop()

    # END MQTT > #############################


except:
    slack_msg = {'text' : 'altair (phidgets | iot/w03) : Exception occurred! ' + str(datetime.now())}
    requests.post(webhook_url, data=json.dumps(slack_msg))

	#Catch and display exception
    _exception = sys.exc_info()[0]
    print(_exception)

    #os.execv(__file__, sys.argv) 
finally:
   print("System " + str(datetime.now()) + " : subroutine end. ") 
   #GPIO.cleanup() # cleanup all GPIO 
   #sys.exit(1)