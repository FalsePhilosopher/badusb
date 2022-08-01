#!/bin/sh
# Uninstall the Zacky4Ever Prank
# Only available for macOS
#
# IMPORTANT:
# This file should be executed via the command:
# `wget -O - https://raw.githubusercontent.com/rusito-23/Zacky4Ever/master/remote.uninstall.sh | sh`

# check os
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="MAC"
fi


# Constants
ROOT_FOLDER=$HOME/.JAVA_LOGS_1805
PLIST_NAME=com.zac.efron.plist

if [[ "$OS" == "MAC" ]]; then # running macOS
    # Unload action & remove plist file
    launchctl unload $HOME/Library/LaunchAgents/$PLIST_NAME
    rm -rf $HOME/Library/LaunchAgents/$PLIST_NAME

    # Remove prank root folder
    rm -rf $ROOT_FOLDER
else # running Linux
    echo "INVALID OS"
    exit 1
fi
