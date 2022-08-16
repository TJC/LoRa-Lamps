#!/bin/bash
x=$(ls -1 /dev/cu.usb*|head -n 1)
export RSHELL_PORT=$x
pushd src
rshell rsync . /pyboard/
popd
