#!/bin/bash
x=$(ls -1 /dev/cu.usbserial-*|head -n 1)
export RSHELL_PORT=$x
pushd src
rshell rsync . /pyboard/
popd
