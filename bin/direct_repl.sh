#!/bin/sh
tty=$(ls -1 /dev/cu.usb*|head -n 1)
screen $tty 115200
