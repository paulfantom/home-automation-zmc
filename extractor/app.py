#!/usr/bin/python

import os
import json
import yaml
import paho.mqtt.client as mqtt

SERVER = ""
INPUT = ""
OUTPUT = ""


def config(path):
    global SERVER, INPUT, OUTPUT
    with open(path, 'r') as stream:
        try:
            conf = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    INPUT = conf['input']
    OUTPUT = conf['output']
    SERVER = conf['server']


def parse(payload):
    actuators = int(payload.decode('UTF-8'))
    status = []
    for i in range(0, 6):
        status.append(actuators & (2**i) != 0)
    return {'burner': int(status[3]),
            'solar_switch': int(status[0]),
            'heater_switch': int(status[2]),
            'solar_pump': int(status[1]),
            'circulation': int(status[4])}


def on_connect(client, userdata, flags, rc):
    client.subscribe(INPUT)


def on_message(client, userdata, msg):
    data = parse(msg.payload)
    client.publish(OUTPUT, json.dumps(data), retain=True)


def main():
    path = os.environ.get('CONFIG_PATH', "config.yml")
    config(path)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(SERVER, 1883)
    client.loop_forever()


if __name__ == '__main__':
    main()
