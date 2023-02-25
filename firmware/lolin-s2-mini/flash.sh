#!/bin/bash
echo "You might need to press the button, then click RST, then release button"
x=$(ls -1 /dev/cu.usb*|head -n 1)
sleep 2
esptool.py --chip esp32s2 --port "$x" --baud 1000000 \
  write_flash -z 0x1000 \
  firmware-lolin-s2-mini-espnow-v1.19.1.bin
