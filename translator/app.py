#!/usr/bin/python

import os
import json
import yaml
import paho.mqtt.client as mqtt

# SERVER = "192.168.2.2"
# DATA = {"temperature": None,
#         "apparent": None,
#         "humidity": None,
#         "pressure": None}
#
# DATA_MAP = {"room/1/temp_real": "temperature",
#             "room/1/temp_feel": "apparent",
#             "room/1/humidity": "humidity",
#             "room/1/pressure": "pressure"}
#
# TOPIC = "room/1/sensor"
SERVER = ""
DATA = {}
DATA_MAP = {}
TOPIC = ""


def config(path):
    global SERVER, DATA, DATA_MAP, TOPIC
    with open(path, 'r') as stream:
        try:
            conf = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    DATA_MAP = conf['map']
    TOPIC = conf['topic']
    SERVER = conf['server']
    for _, value in DATA_MAP.items():
        DATA[value] = None


def check(data):
    for _, value in data.items():
        if value is None:
            return False
    return True


def parse(topic, payload):
    global DATA
    key = DATA_MAP[str(topic)]
    try:
        DATA[key] = float(payload.decode('UTF-8'))
    except ValueError:
        DATA[key] = payload

def zero_data():
    global DATA
    for key, _ in DATA.items():
        DATA[key] = None


def on_connect(client, userdata, flags, rc):
    for topic, _ in DATA_MAP.items():
        client.subscribe(topic)
    return True


def on_message(client, userdata, msg):
    parse(msg.topic, msg.payload)
    if check(DATA):
        client.publish(TOPIC, json.dumps(DATA), retain=True)
        zero_data()


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
