#!/bin/sh
# Setup Zacky Prank
#
# IMPORTANT:
# This file should be executed via the command:
# `wget -O - https://raw.githubusercontent.com/rusito-23/Zacky4Ever/master/remote.install.sh | sh`

GH_REPO_URL=https://github.com/rusito-23/Zacky4Ever.git
REPO_PATH=$HOME/Zacky4Ever

# INSTALL
git clone $GH_REPO_URL $REPO_PATH
cd $REPO_PATH
sh install.sh

# REMOVE ALL TRACES
cd $HOME
rm -rf $REPO_PATH
