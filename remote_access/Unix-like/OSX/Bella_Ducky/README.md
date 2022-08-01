# Bella Ducky Script for USB Rubber Ducky from Hak5
This Ducky Script will download a `.zip` file from your server to the target machine, unzip it, run Bella, clean up the install files, and then quit Terminal.

# Requirements:
- A server to hold your `.zip` file
- Bella (Local machine for building payloads and remotely accessible server for C&C)
- Bella build configured with your settings
- USB Rubber Ducky from Hak5

# Instructions:
1. Clone Bella (https://github.com/dayofdoom/Bella) and run the `./BUILDER` tool to build your payload.
2. Compress the Bella file created in `/Bella-master/Builds/xx-xx@xx_xx/Bella` and name it `Bella.zip`.
3. Upload `Bella.zip` to your server.
4. Modify Bella Ducky Script to point to the location of your server (`https://myserver.com/Bella/Bella.zip`)
5. Copy/Paste to the Duck ToolKit Encoder (https://ducktoolkit.com/encoder/). Click Generate and download the `inject.bin` file.
6. Copy `inject.bin` to your Ducky's SD card.
7. Plug the Rubber Ducky into a test target computer. Verify everything is working.
8. Open up Bella's C&C and wait for the target to connect.

# Support
- Bella repo: https://github.com/dayofdoom/Bella
- Duck Toolkit: https://ducktoolkit.com/
- Hak5 USB Rubber Ducky: https://hakshop.com/collections/usb-rubber-ducky

# Project Notes

*10/19/2020
*As this Bella software is over 4 years old, I can't vouch for it's use on new macOS systems. Please use as an educational resource and not as a current pentesting tool. However, the DuckyScript is still valid.

The orignal Bella repo has been removed. Please use my fork (or others found on github).
