
# import libraries
# import boto3
import json
import time
# from datetime import datetime
# import requests
# import os
# import sys
import random
import paho.mqtt.client as mqtt

# setup MQTT broker instance
THINGSBOARD_HOST = '13.58.203.102'
client1 = mqtt.Client()
pk1 = '3D7lkczBsjPkfIyOyqDp'
client1.username_pw_set(pk1)


# hardcoded coordinates - to be changed when we get actual sensor data
coordinates = [[-84.27532, -84.277338, -84.27878, -84.280646, -84.281101,
                -84.282027, -84.283817, -84.285881, -84.285281, -84.283294,
                -84.280987, -84.279326, -84.277490],
               [34.05473, 34.054567, 34.053404, 34.050444, 34.050111, 34.051035,
                34.050632, 34.050865, 34.052851, 34.052757, 34.052380, 34.05204,
                34.054278]]


while coordinates:
    # connecting to MQTT broker
    client1.connect(THINGSBOARD_HOST, 1883, 60)

    for i in range(0, 12):
        temp = {u"ID": 2645, u"lon": coordinates[0][i],
                u"lat": coordinates[1][i], u"Temp": random.randint(51, 65)}
        print(json.dumps(temp))

        # publishing data
        client1.publish('v1/devices/me/telemetry', json.dumps(temp), 1)
        time.sleep(10)
