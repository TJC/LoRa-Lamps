#!/bin/bash
x=$(ls -1 /dev/cu.usb*|head -n 1)
echo "Hold button 9, press button RST, release button 9"
sleep 2
esptool.py --chip esp32-c3 --port "$x" erase_flash
