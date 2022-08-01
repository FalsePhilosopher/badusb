#!/bin/bash
while [ true ]
do
netcat -vlp 1337 &>> passwd.txt
done
