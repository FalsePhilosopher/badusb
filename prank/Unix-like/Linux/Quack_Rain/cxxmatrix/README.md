# C++ Matrix in terminal

I wrote a simple terminal program of Matrix digital rain.
A part of the purpose of this program is to test the performance of terminal emulators.
Another purpose is just for fun.
Enjoy it with fast terminals (e.g., urxvt, alacritty, terminology, etc.)!

**Features**

- Hankaku kana characters as in the original film
- Ten levels of "green"s using terminal 256 color support
- Twinkling effects by adding random brightness fluctuations
- Diffused reflection effects by cell background colors

**Scenes**

By default, the following scenes will be visited in turn.
If you want to see each scene, please see the help (`cxxmatrix --help`).

1. Number falls
2. Banner - Show command line arguments by shining characters
3. "The Matrix" rain - [Wikipedia](https://en.wikipedia.org/wiki/Matrix_digital_rain)
4. Conway's Game of Life - [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
5. The Mandelbrot set - [Wikipedia](https://en.wikipedia.org/wiki/Mandelbrot_set)
6. (End scene) "The Matrix" rain

## Demo

- cxxmatrix in 80x28 - [Youtube](https://www.youtube.com/watch?v=DeKuT8txldc)
- The Mandelbrot set in 479x186 - [YouTube](https://www.youtube.com/watch?v=RtMy4ltebKw)
- Highlight scenes - See the animated GIF below

![Captures](https://raw.githubusercontent.com/wiki/akinomyoga/cxxmatrix/images/cxxmatrix-version01sA.gif)

## Usage

This program is provided under the [MIT License](LICENSE.md).

### Prerequisites

- git, C++17 compiler, GNU make, GNU awk
- UTF-8 support of the system
- a fast terminal with `256color` and UTF-8 support

### Compile and Run

```bash
$ git clone https://github.com/akinomyoga/cxxmatrix.git
$ cd cxxmatrix
$ make
$ ./cxxmatrix 'The Matrix' 'Reloaded'
```

Quit: <kbd>C-c</kbd>; Suspend: <kbd>C-z</kbd>; Menu: <kbd>RET</kbd>, <kbd>C-m</kbd>


**Compile MSYS2 binary (MSYS2 PTY) using MSYS2**

The MSYS package `msys2-devel` is required in order to use the MSYS2 compiler.

```bash
msys2$ pacman -Syu
msys2$ pacman -S git gawk make msys2-devel
msys2$ git clone https://github.com/akinomyoga/cxxmatrix.git
msys2$ cd cxxmatrix
msys2$ PATH=/usr/bin:$PATH make
```

**Compile Windows binary (ConPTY) using MinGW/MSYS2**

The Windows binary based on Windows Pseudo Console API (ConPTY) can be compiled on MinGW/MSYS2 by passing `TARGET=win32` to `make`.
It should be noted that ConPTY is extremely slow.

```bash
msys2$ pacman -Syu
msys2$ pacman -S git gawk make mingw-w64-x86_64-gcc
msys2$ git clone https://github.com/akinomyoga/cxxmatrix.git
msys2$ cd cxxmatrix
msys2$ PATH=/mingw64/bin:$PATH make TARGET=win32
```

### Options

Check the help with `cxxmatrix --help`:

```console
$ ./cxxmatrix --help
cxxmatrix (C++ Matrix)
usage: cxxmatrix [OPTIONS...] [[--] MESSAGE...]

MESSAGE
   Add a message for 'banner' scene.  When no messages are specified, a
   message "C++ MATRIX" will be used.

OPTIONS
   --help      Show help
   --          The rest arguments are processed as MESSAGE
   -m, --message=MESSAGE
               Add a message for 'banner' scene.
   -s, --scene=SCENE
               Add scenes. Comma separated list of 'number', 'banner', 'rain',
               'conway', 'mandelbrot', 'rain-forever' and 'loop'.
   -c, --color=COLOR
               Set color. One of 'default', 'black', 'red', 'green', 'yellow',
               'blue', 'magenta', 'cyan', 'white', integer 0-255 (256 index
               color), '#RGB', and '#RRGGBB'.
   --colorspace=COLORSPACE
               Set colorspace. One of 'default'/'xterm-256'/'256',
               'ansi-8'/'8', 'aix-16'/'16', 'xterm-88'/'88', 'xterm-rgb',
               'iso-rgb'/'rgb', 'iso-cmy'/'cmy', 'iso-cmyk'/'cmyk', or
               'iso-index'/'index'.
   --frame-rate=NUM
               Set the frame rate per second.  A positive number less than or
               equal to 1000. The default is 25.
   --error-rate=NUM
               Set the factor for the rate of character changes.  A
               non-negative number.  The default is 1.0.
   --diffuse
   --no-diffuse
               Turn on/off the background-color effect.  Turned on by default.
   --twinkle
   --no-twinkle
               Turn on/off the twinkling effect.  Turned on by default.
   --preserve-background
   --no-preserve-background
               Preserve terminal background or not.  Not preserve by default.
   --rain-density=NUM
               Set the factor for the density of rain drops.  A positive
               number.  The default is 1.0.

Keyboard
   C-c (SIGINT), q, Q  Quit
   C-z (SIGTSTP)       Suspend
   C-m, RET            Show menu
```

**Select scenes**

```bash
# Example: Show the Mandelbrot set
./cxxmatrix -s mandelbrot

# Example: Loop Number falls and Conway's Game of Life
./cxxmatrix -s number,conway,loop
```

## Install


```bash
sudo make install
```

The default install prefix is `/usr/local`. The following files will be created:

- `/usr/local/bin/cxxmatrix`
- `/usr/local/share/man/man1/cxxmatrix.1.gz`
- `/usr/local/share/licenses/cxxmatrix/LICENSE.md`

The make variable `PREFIX` can be specified to change the install prefix.
To copy files in a temporary location, the make variable `DESTDIR` can also be specified.
To change the subdirectory of `LICENSE.md`, the make variable `INSTALL_SUBDIR_LICENSE` (whose detault value is `share/licenses/cxxmatrix`) can be adjusted.

```bash
# Example 1: install cxxmatrix in user directory
make install PREFIX=~/.local

# Example 2: install cxxmatrix in /opt
sudo make install PREFIX=/opt/cxxmatrix

# Example 3: create a package
make install DESTDIR=/tmp/packages/cxxmatrix PREFIX=/usr/local

# Example 4: put LICENSE.md in /usr/local/share/cxxmatrix
sudo make install INSTALL_SUBDIR_LICENSE=share/cxxmatrix
```

### See also

- AUR Package: [AUR (en) - cxxmatrix-git](https://aur.archlinux.org/packages/cxxmatrix-git/) by @ignapk
- FreeBSD Package: [misc/cxxmatrix](https://www.freshports.org/misc/cxxmatrix) by @nunotexbsd (`Nuno Teixeira <eduardo@FreeBSD.org>`)

# Similar projects

Related tags in GitHub:

- [`#matrix-rain`](https://github.com/topics/matrix-rain)
- [`#matrix-digital-rain`](https://github.com/topics/matrix-digital-rain)

In each section, the projects are ordereded by the number of stars, which is shown in parentheses for each project.
This list including the numbers of stars is updated when `cxxmatrix` is updated so does not reflect the current status.
The numbers of stars are last updated on 2022-03-24 19:57:14 JST.

## The Matrix rains in terminals

- [abishekvashok/cmatrix](https://github.com/abishekvashok/cmatrix) - [Demo](https://github.com/abishekvashok/cmatrix#screencasts) in C (2547)
- [will8211/unimatrix](https://github.com/will8211/unimatrix) - [Demo](https://github.com/will8211/unimatrix#screenshots) in Python3 (1389)
- akinomyoga/cxxmatrix - [HN](https://news.ycombinator.com/item?id=22510839) in C++ (573)
- [nojvek/matrix-rain](https://github.com/nojvek/matrix-rain) - [Demo](https://github.com/nojvek/matrix-rain#screenshots) in Node (399)
- [st3w/neo](https://github.com/st3w/neo) - [Demo](https://github.com/st3w/neo#neo), [Reddit 1](https://www.reddit.com/r/unixporn/comments/rh45qv/oc_recreate_the_digital_rain_from_the_matrix_in/) [2](https://www.reddit.com/r/linux/comments/rhwqu5/wake_up_neo/) [3](https://www.reddit.com/r/SideProject/comments/rgnq0m/neo_recreate_the_digital_rain_from_the_matrix_in/) [4](https://www.reddit.com/r/terminal_porn/comments/rgoj5f/neo_recreate_the_digital_rain_from_the_matrix_in/) in C++ (342)
- [M4444/TMatrix](https://github.com/M4444/TMatrix) - [Demo](https://github.com/M4444/TMatrix#how-it-looks), [Reddit](https://www.reddit.com/r/unixporn/comments/btg6rj/oc_tmatrix_a_new_terminal_digital_rain_simulator/) in C++ (280)
- [GeertJohan/gomatrix](https://github.com/GeertJohan/gomatrix) - [Youtube](https://www.youtube.com/watch?v=mUXFxSmZMis) in Go (244)
- [cowboy8625/rusty-rain](https://github.com/cowboy8625/rusty-rain) - [Demo](https://github.com/cowboy8625/rusty-rain#----------rusty-rain----), [Reddit](https://www.reddit.com/r/rust/comments/llauze/cross_platform_matrix_rain/) in Rust (109)
- [levithomason/cmatrix](https://github.com/levithomason/cmatrix) - [Demo](https://github.com/levithomason/cmatrix#cmatrix) in C (73)
- [torch2424/wasm-matrix](https://github.com/torch2424/wasm-matrix) - [Demo](https://github.com/torch2424/wasm-matrix#wasm-matrix) in WASM (61)
- [jsbueno/terminal_matrix](https://github.com/jsbueno/terminal_matrix) - [Demo](https://github.com/jsbueno/terminal_matrix#python-script-to-simulate-the-matrix-screensaver-effect-in-a-posix-terminal) in Python (52)
- [joechrisellis/pmatrix](https://github.com/joechrisellis/pmatrix) - [Demo](https://github.com/joechrisellis/pmatrix#pmatrix-in-action) in Python (35)
- [domsson/fakesteak](https://github.com/domsson/fakesteak) - [Demo](https://github.com/domsson/fakesteak#fakesteak), [Reddit](https://www.reddit.com/r/unixporn/comments/ju62xa/oc_fakesteak_yet_another_matrix_rain_generator/) in C (35)
- [amstrad/oh-my-matrix](https://github.com/amstrad/oh-my-matrix) - [Demo](https://github.com/amstrad/oh-my-matrix/blob/master/oh-my-matrix.gif) in Python (20)
- [b166erbot/matrix](https://github.com/b166erbot/matrix) in Python3 (18)
- [meganehouser/rustmatrix](https://github.com/meganehouser/rustmatrix) - [Demo](https://github.com/meganehouser/rustmatrix#rustmatrix) in Rust (17)
- [txstc55/matrix_viewer](https://github.com/txstc55/matrix_viewer) - [Demo](https://github.com/txstc55/matrix_viewer#matrix-viewer) in C++ (15)
- [henriquebastos/the-matrix-rain](https://github.com/henriquebastos/the-matrix-rain) - [Demo](https://github.com/henriquebastos/the-matrix-rain#the-matrix-rain) in Python (9)
- [aguegu/greenrain](https://github.com/aguegu/greenrain) - [Demo](https://github.com/aguegu/greenrain#greenrain) in C++ (7)
- [JaydenL33/cmatrix2.0](https://github.com/JaydenL33/cmatrix2.0) in C (3)
- [kevinelong/rain](https://github.com/kevinelong/rain) [Demo](https://github.com/kevinelong/rain#rain), [Youtube](https://www.youtube.com/watch?v=w4mc2xnIKBY), [Reddit](https://www.reddit.com/r/Simulated/comments/l49svb/rain_simulation_on_amber_terminal_window_that_is/) - in Python (3)
- [stefrush/enterthematrix](https://github.com/stefrush/enterthematrix) - [Demo](https://github.com/stefrush/enterthematrix#enterthematrix) in Python (2)
- [Shizcow/smatrix](https://github.com/Shizcow/smatrix) in Rust (1)
- [gurushida/matrixmirror](https://github.com/gurushida/matrixmirror) - [Demo](https://github.com/gurushida/matrixmirror#matrixmirror) in Objective-C (0)
- [roee30/rmatrix](https://github.com/roee30/rmatrix) in Rust (0)

## The Matrix rains in browsers

- [tidwall/digitalrain](https://github.com/tidwall/digitalrain) - [Demo](https://tidwall.com/digitalrain/) in HTML5 Canvas (360)
- [emilyxxie/green_rain](https://github.com/emilyxxie/green_rain) - [Demo](http://xie-emily.com/generative_art/green_rain.html) in HTML5 Canvas (246)
- [Rezmason/matrix](https://github.com/Rezmason/matrix) - [Demo](https://rezmason.github.io/matrix/), [HN](https://news.ycombinator.com/item?id=28446761) in HTML5 Canvas (204)
- [winterbe/github-matrix](https://github.com/winterbe/github-matrix) - [Demo](https://winterbe.com/projects/github-matrix/) in HTML5 Canvas (194)
- [neilcarpenter/Matrix-code-rain](https://github.com/neilcarpenter/Matrix-code-rain) - [Demo](http://neilcarpenter.com/demos/canvas/matrix/) in HTML5 Canvas (100)
- [syropian/HTML5-Matrix-Code-Rain](https://github.com/syropian/HTML5-Matrix-Code-Rain) - [Demo](https://codepen.io/syropian/pen/bLzAi) in HTML5 Canvas (34)
- [raphaklaus/matrix-fx](https://github.com/raphaklaus/matrix-fx) - [Demo](https://raphaklaus.com/matrix-fx/) in CSS3 (28)
- [pazdera/matrix-vr](https://github.com/pazdera/matrix-vr) - [Demo](https://radek.io/matrix-vr/) in WebVR (22)
- [lhartikk/BtcTxMatrix](https://github.com/lhartikk/BtcTxMatrix) - [Demo](http://lhartikk.github.io/btctxmatrix/) in HTML5 Canvas (14)
- [anderspitman/redpill](https://github.com/anderspitman/redpill) - [Demo](https://anderspitman.net/apps/redpill/) in HTML5 Canvas (9)
- [pmutua/Matrix-Rain](https://github.com/pmutua/Matrix-Rain) - [Demo](https://pmutua.github.io/Matrix-Rain/) in HTML5 Canvas (2)
- [zhaihaoran/digital-rain](https://github.com/zhaihaoran/digital-rain) - [Demo](https://zhaihaoran.github.io/digital-rain/) in HTML5 Canvas (3)
- [Workvictor/pixi-digital-rain](https://github.com/Workvictor/pixi-digital-rain) - [Demo](https://victorpunko.ru/development/digital-rain-v3/) in HTML5 Canvas (0)
- [azder/ES2017-Matrix-Rain](https://github.com/azder/ES2017-Matrix-Rain) - [Demo](https://azder.github.io/ES2017-Matrix-Rain/) in HTML5 Canvas (0)
- [codingotaku/7-Segment-Digital-Matrix-Rain](https://github.com/codingotaku/7-Segment-Digital-Matrix-Rain) - [Demo](https://codingotaku.com/7-Segment-Digital-Matrix-Rain/) in HTML5 Canvas (0)

## Others

- [winterbe/github-matrix-screensaver](https://github.com/winterbe/github-matrix-screensaver) (github-matrix/WebSaver?) in JavaScript (502)
- [tremby/Kaleidoscope-LEDEffect-DigitalRain](https://github.com/tremby/Kaleidoscope-LEDEffect-DigitalRain) in Kaleidoscope? (22)
- [nathanchere/MatrixSaver](https://github.com/nathanchere/MatrixSaver) in C# (22)
- [sapandang/Matrix-Rain-Live-Wallpaper](https://github.com/sapandang/Matrix-Rain-Live-Wallpaper) in Android Wallpaper (16)
- [Sullivan008/CSharp-MatrixRain](https://github.com/Sullivan008/CSharp-MatrixRain) in C# (1)
- [artgl42/MatrixDigitalRain](https://github.com/artgl42/MatrixDigitalRain) - [Demo](https://github.com/artgl42/MatrixDigitalRain#matrixdigitalrain-dll) in C# (0)

## Videos

- [Chuvas da Matrix - YouTube](https://www.youtube.com/watch?v=y9wD8Nck1VA)
