#!/bin/bash
x=$(ls -1 /dev/cu.usb*)
for port in $x; do
  export RSHELL_PORT="$port"
  pushd src
  rshell rsync . /pyboard/
  popd
done
