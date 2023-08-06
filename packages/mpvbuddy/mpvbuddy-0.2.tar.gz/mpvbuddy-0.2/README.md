# mpvbuddy

Mpvbuddy is a frontend for the media player [mpv](https://mpv.io). It's main feature is the ability to keep track of where you are in every video on your playlist so you can jump around between videos you are currently watching. It supports multiple playlists as well.

It's still in early beta and is written in Python + PyQt5. Please include and messages from the console and logging window (Ctrl+U) when filing issues.

# Installation and Usage

You should have Qt installed (5.11.3 or higher is recommended) using your distributions default package manager, as well as PyQt5-5.10 or higher. All other dependencies can be taken care of by pip and installed to your home directory. Assuming you haven't adjusted your `XDG_` environment variables, the following should install and run mpvbuddy:

```
pip3 install --user mpvbuddy
~/.local/bin/mpvbuddy

```

# License

mpvbuddy is licensed under the GNU GPLv3 (2019). Dependencies and their licenses can be found in the about dialog. 
