# Rubber Ducky Password Stealer
file:///home/user/Downloads/Flipper/BadUSBgit/Rubber_Ducky_Password_Stealer

With this software it is possible to retrieve user passwords from a Windows 10/11 system. For example, passwords from browsers, installed programs and system saved passwords such as WiFi passwords. In addition, there is also an optional option to add scripts that retrieve system information, program information, network information, etc. It is also possible to add your own .bat scripts that are automatically executed next to the current scripts.

The above data is stored in text files on the SD card of the Rubber Ducky. This data is stored in a folder with the target's computer and username so that there are no complications when running on multiple computers or user accounts.

The Twin Duck firmware, custom payload, custom scripts and third party programs made it possible to achieve this. Thanks to the external parties mentioned on this GitHub page who are an important part of this software.

I am not responsible for damage affected by this software to your own or other systems. The purpose of this software is to recover forgotten passwords, improve your own digital security and gain knowledge about a Rubber Ducky, the Twin Duck firmware, writing scripts in combination with the use of external programs etc. It is not intended to be used for malicious purposes.

## Requirements

- [Rubber Ducky](https://hak5.org/collections/sale/products/usb-rubber-ducky-deluxe) with the [Twin Duck firmware](https://raw.githubusercontent.com/hak5darren/USB-Rubber-Ducky/master/Firmware/Images/c_duck_v2.1.hex) installed (Open link, Ctrl+S to save file).
- Micro SD card (Default 128mb micro SD card didn't work in my case).

## Compatibility

- Windows 10/11 x32/x64.
- Windows Security must be used as virus scanner for this software to work.
- Successful operation on the target system depending on the language support of the payload.
- This software can only be executed if the user has unlocked his system.
- This software (unchanged) only works on systems that are not too slow to perform the slow payload version and the external software within a certain time.

## Setup Rubber Ducky environment

1. Rename the label of the Rubber Ducky storage to: "RDPS".
2. Download the [latest release](https://github.com/Krouwndouwn/Rubber_Ducky_Password_Stealer/releases/latest) (environment and scrips, payload with the right language (a payload equal to the target system) and extra scripts for getting system information (optional)) and extract the rar files to the root location of the Rubber Ducky storage.
3. Disable Windows Security otherwise the downloaded files will be removed from the system in the next steps.
4. Download the [Windows Password Recovery Tools](https://www.nirsoft.net/password_recovery_tools.html) with command-line support from Nirsoft and extract them to: "(Rubber Ducky storage)\files\nirsoft\".
5. Manualy download the command-line tools: BulletsPassView ([x32](https://www.nirsoft.net/utils/bulletspassview.zip)/[x64](https://www.nirsoft.net/utils/bulletspassview-x64.zip)), OperaPassView ([x32](https://www.nirsoft.net/toolsdownload/operapassview.zip)), RouterPassView ([x32](https://www.nirsoft.net/toolsdownload/routerpassview.zip)) and WirelessKeyView ([x32](https://www.nirsoft.net/toolsdownload/wirelesskeyview.zip)/[x64](https://www.nirsoft.net/toolsdownload/wirelesskeyview-x64.zip), password: "WKey4567#"). Also extract the downloaded x32 files (only the .exe files) to: "(Rubber Ducky storage)\files\nirsoft\".
6. Rename the just downloaded x64 files to: "(filename)_x64.exe" and move them to: "(Rubber Ducky storage)\files\nirsoft\" Also do this for the x64 files located in: "(Rubber Ducky storage)\files\nirsoft\x64\" and remove the x64 folder afterwards. Feel free to delete Nirsoft files that are of no use to you. Learn more about what these files do on the [Nirsoft website](https://www.nirsoft.net/).
7. Rename all extrensions of the files located in: "(Rubber Ducky storage)\files\nirsoft\" from: ".exe" to: ".rdps". The idea behind this is to reduce Windows Security's alertness to these files when the Rubber Ducky is just plugged into the target system.
8. Download the [mimikatz](https://github.com/gentilkiwi/mimikatz/releases) tool and extract it to: "(Rubber Ducky storage)\files\mimikatz\".
9. Rename the extension of the "mimikatz.exe" files located in: "(Rubber Ducky storage)\files\mimikatz\Win32\" and "(Rubber Ducky storage)\files\mimikatz\x64\" from: ".exe" to: ".rdps".
10. Safely remove the Rubber ducky storage.
11. Turn Windows Security back on.
12. The Rubber Ducky environment has now been fully set up and can be used.

Update this software and external programs mentioned above regularly for desired results.

## Usage

1. Make sure the Rubber Ducky environment is set up correctly.
2. Place the Rubber Ducky in the target system.
3. Wait about 60 seconds until everything has been executed. When a Caps Lock light is present, it will flash a number of times to indicate that it is finished.
4. Remove the Rubber Ducky from the target system.
5. If all went well, the Rubber Ducky has now saved the results in the result folder.

## Make your own changes

**Optimize speed**

- Remove unnecessary executable programs (Nirsoft and/or mimikatz) and scripts that increase the execution time of the software.
- Set the "Wait Until Everything is executed" inside the payload properly to the time how long it takes to perform all programs and scripts.
- Reduce the waiting times (DELAY) in the payload where this is possible so that the payload can execute faster on the target system. This depends on the speed of the target system.

**Add programs and scripts**

- Add your own .bat scripts that are automatically executed when placed in the: "(Rubber Ducky storage)\files\scripts\" folder.
- Add your own programs in the "(Rubber Ducky storage)\files\(new folder)\" folder that can be controlled by their own .bat script.

**Change virus scanner**

- Change the payload script to disable another virusscanner. It may be possible to disable another virus scanner by adding scripts or executable programs.

**Change everything**

- Re-writing or reuse the payload and scripts to write new software that contains a different goal. For example, automating certain installations or automatically changing settings in Windows.

## Issues

Please feel free to [submit an issue](https://github.com/Krouwndouwn/Rubber_Ducky_Password_Stealer/issues/new/choose) for any of the following reasons:

- Reporting a bug.
- Reporting a grammatical error.
- Suggesting a feature.
- Suggesting a improvement.
- Any other issue with the payloads, scripts or GitHub page.

## FAQ

**How can i rename file extensions?**

Open Windows file explorer, open the "View" tab and enable: "File name extensions". Then just simply replace the extension name.

**How do I generate my own payload?**

Create a text file and converts it through the [Duck Encoder](https://github.com/hak5darren/USB-Rubber-Ducky/releases) to a .bin file. Or use the online [Duck Toolkit](https://ducktoolkit.com/encode) for this.
