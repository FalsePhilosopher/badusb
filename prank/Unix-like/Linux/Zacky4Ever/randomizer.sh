#!/bin/sh 
# Selects a random file from the given folder
# Parameter $1 -> Source Folder

ROOT_FOLDER=$1
files=($ROOT_FOLDER/*)
printf "%s\n" "${files[RANDOM % ${#files[@]}]}"
