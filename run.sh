#!/bin/bash

function start() {
    docker run -d --name mosquitto --rm -p 1883:1883 eclipse-mosquitto || exit 1
	IP="$(docker inspect -f '{{ .NetworkSettings.IPAddress }}' mosquitto)"
    sleep 1
    for device in weather room tank solar heater circulate
    do
    	sed -i "s/^server:.*$/server: $IP/" "$(pwd)/configs/${device}.yml"
        docker run -d --rm --name "${device}" \
        	       -v "$(pwd)/configs/${device}.yml:/usr/src/app/config.yml" \
        	       paulfantom/mqtt_translator &
    done
    sed -i "s/^server:.*$/server: $IP/" "$(pwd)/extractor/config.yml"
    docker run -d --rm --name actuators \
    	       -v "$(pwd)/extractor/config.yml:/usr/src/app/config.yml" \
    	       paulfantom/mqtt_extractor &
    wait

    python simulator/app.py
    mosquitto_sub -v -t '#' -h localhost
}

function stop() {
    for container in weather room tank solar heater circulate actuators mosquitto
    do
	    docker stop "${container}" &
    done
    wait
}

case "$1" in
	"stop") stop ;;
	*) start ;;
esac
