#!/usr/bin/python

import paho.mqtt.client as mqtt
import time

SERVER = "localhost"
MAP = {
    "solarControl/heater/settings/schedule":
    '{"week":[0,0,0,0,0,1,1],"work":[{"to":[6,30],"from":[5,30],"temp":21.9},{"to":[21,45],"from":[14,0],"temp":22.6}],"other":18.0,"free":[{"to":[22,0],"from":[6,30],"temp":22.1}]}',
    "room/1/temp_real": 22.0,
    "room/1/temp_feel": 21.3,
    "room/1/humidity": 40.9,
    "room/1/pressure": 1015.5,
    "room/1/temp_current": 22.0,
    "solarControl/solar/temp": 21.89,
    "outside/temp": -3.38,
    "solarControl/solar/temp_in": 26.39,
    "solarControl/solar/temp_out": 18.66,
    "solarControl/heater/temp_in": 47.86,
    "solarControl/heater/temp_out": 32.68,
    "solarControl/tank/temp_up": 41.64,
    "solarControl/circulate/pump": 0,
    "solarControl/actuators": 3,
    "solarControl/solar/pump": 30 }

def main():
    client = mqtt.Client()
    client.connect(SERVER, 1883)
    client.loop_start()
    for k, v in MAP.items():
        client.publish(k, v, retain=True)
        time.sleep(0.01)


if __name__ == '__main__':
    main()
