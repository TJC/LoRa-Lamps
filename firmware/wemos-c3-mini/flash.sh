#!/bin/bash
echo "Hold button 9, press button RST, release button 9"
sleep 2
esptool.py --chip esp32-c3 --port /dev/cu.usbmodem2101 --baud 1000000 \
	write_flash -z 0 \
	firmware-lolin-c3-mini-espnow-v1.19.1.bin 
