#!/bin/bash
if [[ -z "$1" ]]; then
	echo "Pass the esp...bin file as a parameter"
	exit 1
fi
echo "Hold down BOOT button for a second..."
tty=$(ls -1 /dev/cu.wch*|head -n 1)
echo "Flashing to $tty"
esptool.py --chip esp32 --port $tty --baud 460800 write_flash -z 0x1000 "$1"
