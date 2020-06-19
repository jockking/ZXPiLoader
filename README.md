# ZXPiLoader
A raspberry pi audio loader for ZX Spectrum games

# Hardware
To make this work i used a usb soundcard with a stereo to dual mono connectors.  One of the connections goes into the EAR socket on the spectrum

# Installation
I've hardcoded lots of values but the roms should go in a folder called roms.  The python script will scan this folder and look for an associated png image with the same file name.  I'm sure there is a much better way to improve all this but this solution met my needs.

This solution was based on a tutorial from:

https://supratim-sanyal.blogspot.com/2020/01/zx-spectrum-tzx-tap-zip-cassette-loader.html
