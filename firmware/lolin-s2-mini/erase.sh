#!/bin/bash
x=$(ls -1 /dev/cu.usb*|head -n 1)
sleep 2
esptool.py --chip esp32s2 --port "$x" erase_flash
