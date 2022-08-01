#!/bin/bash

cd -- "$(dirname "$BASH_SOURCE")"
python install_cron.py
cd ../
cwd=$(pwd)
diskutil unmount $cwd
killall Terminal
