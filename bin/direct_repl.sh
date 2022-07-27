#!/bin/sh
tty=$(ls -1 /dev/cu.usbserial-*|head -n 1)
screen $tty 115200
