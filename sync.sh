#!/bin/bash

OPERATION=$1
HOSTNUM=$2

# ensure args passed
if [[ -z "$HOSTNUM" || -z "${OPERATION}" ]]; then
	echo "usage: ./sync.sh <operation=push|pull> <host_num=0|1>"
	exit 1
fi

# ensure hostnum is valid
if [[ "${HOSTNUM}" -ne "1" && "${HOSTNUM}" -ne "0" ]]; then
    echo "host_num must be 0 or 1"
    exit 1
fi

HOSTNAME="raspberrypi${HOSTNUM}.local"
REMOTE_DIR="pi@${HOSTNAME}:/home/pi/floasis-raspi/"  # trailing slash so copy files not dir
LOCAL_DIR="$(pwd)"
RSYNC_OPTS="-avz"

if [[ "${OPERATION}" = "push" ]]; then
    echo "PUSH -> ${HOSTNAME}"
    rsync ${RSYNC_OPTS} ${LOCAL_DIR}/ ${REMOTE_DIR}  # trailing slash so copy files not dir
elif [[ "${OPERATION}" = "pull" ]]; then 
    echo "PULL <- ${HOSTNAME}"
    rsync ${RSYNC_OPTS} ${REMOTE_DIR} ${LOCAL_DIR}
else
    echo "invalid operation"
    exit 1
fi
