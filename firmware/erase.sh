#!/bin/bash
echo "Hold down BOOT button for a second..."
tty=$(ls -1 /dev/cu.usbserial*|head -n 1)
echo "Flashing to $tty"
esptool.py --chip esp32 --port $tty erase_flash
