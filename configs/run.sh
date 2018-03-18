#!/bin/bash
docker run -d --rm --name weather -v "$(pwd)/weather.yml:/usr/src/app/config.yml" paulfantom/mqtt_translator
docker run -d --rm --name room -v "$(pwd)/room_sensor.yml:/usr/src/app/config.yml" paulfantom/mqtt_translator
docker run -d --rm --name tank -v "$(pwd)/tank.yml:/usr/src/app/config.yml" paulfantom/mqtt_translator
docker run -d --rm --name solar -v "$(pwd)/solar.yml:/usr/src/app/config.yml" paulfantom/mqtt_translator
docker run -d --rm --name heater -v "$(pwd)/heater.yml:/usr/src/app/config.yml" paulfantom/mqtt_translator
docker run -d --rm --name circulate -v "$(pwd)/circulate.yml:/usr/src/app/config.yml" paulfantom/mqtt_translator
docker run -d --rm --name actuators paulfantom/mqtt_extractor
