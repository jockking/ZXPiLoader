#!/bin/bash

sudo apt-get install audacious texinfo build-essential automake git
git clone https://github.com/ralferoo/cpctools
cd cpctools/playtzx-0.12b/
./configure
make
sudo make install

#Not liking unnecessary write cycles to the MicroSD card, I created a 128 MB in-memory ramdisk for writing temporary VOC files
sudo mkdir /ram0
#Add the following to /etc/fstab 'tmpfs /ram0 tmpfs nodev,nosuid,size=128M 0 0' 
