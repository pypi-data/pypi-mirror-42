# stallyns

Web app user switcher for RetroPie/EmulationStation.

![screenshot][screenshot]

## What it is

stallyns lets you have separate ROM directories for different users of your system.

For now, it is expected that you have all of your ROMs stored in 'user' directories at \~/roms. See below:

    /home/pi/roms/
    ├── kids
    │   ├── atari2600
    │   ├── mame-libretro
    │   ├── ports
    │   └── saves
    └── me
        ├── atari2600
        ├── mame-libretro
        ├── ports
        └── saves

## Installation

    $ pip install --upgrade stallyns

or clone this repo and install:

    $ git clone https://github.com/dlawregiets/stallyns && cd stallyns && pip install .

## Running

Copy the stallyns.service file to \~/.config/systemd/stallyns.service. Reload systemd for the user and then activate and start the service:

    systemctl --user daemon-reload
    systemctl --user enable --now stallyns.service

## Usage

After installing, navigate to <http://pi:5000>. A list of users will be displayed at the top along with a list of system options at the bottom (useful for if your kids won't turn off the games and you just want to shut the whole thing down).

On your first run, all user buttons will be white. When a user directory is symlinked to ~/RetroPie/roms, their button will be blue.

On the initial user selection in stallyns, \~/RetroPie/roms is moved to ~/RetroPie/roms.orig and a symlink is created from *\~/roms/USER* to *\~/RetroPie/roms*.

## Issues

I recommend that you quit games before switching users. Killing the active running retroarch or other running application seems to lead to funky states of the display and a restart of EmulationStation does not fix it.

## Save States (optional)

I prefer to keep my save state and save files separate from the ROMs, so I do the following:

Modify /opt/retropie/configs/all/retroarch/retroarch.cfg to set the following:

    savefile_directory = "/home/pi/RetroPie/roms/saves/"
    savestate_directory = "/home/pi/RetroPie/roms/saves/"


[screenshot]: https://github.com/dlawregiets/stallyns/raw/master/resources/screenshot.png