#!/bin/bash
# playcdt: script bash to play TZX/CDT tape images of Amstrad CPC & ZX Spectrum
# requires playtzx and audacious (see http://malagaoriginal.blogspot.com.es)
# version 0.1 alpha - GNU/GPL 2 Jesus Basco 2016
# modified by Supratim Sanyal - see https://supratim-sanyal.blogspot.com/2019/12/zx-spectrum-tzx-tap-zip-cassette-loader.html

volume="90%"

# Set volume of USB sound card to 90%
echo ====
echo Setting volume
amixer -c 1 cset numid=6 ${volume},${volume}
amixer -c 1 cget numid=6
echo ====


es_zit=$(file -b "$1" | grep -i zip | wc -l)
es_tzx=$(file -b "$1" | grep -i tzx | wc -l)
#tmptzx=/tmp
#USE Ramdisk instead of wearing out SD
tmptzx=/ram0
if [ $# -ne 1 ]; then
   echo "ERROR: Hay que poner el archivo TZX/CDT"
   exit -1
fi
if [ -f "$1" ]; then
   if [ $es_tzx == 1 ]; then
      echo Reproduciendo archivo \""$1"\"
      playtzx -voc -freq 32000 "$1" ${tmptzx}/temporal.voc

      echo
      echo ==== Playing converted file  ====
      ls -lh ${tmptzx}/temporal.voc
      echo =================================
      echo

      audacious -pqH ${tmptzx}/temporal.voc
      #rm ${tmptzx}/temporal.voc
   elif [ $es_zip == 1 ]; then
      echo AVISO: El archivo \""$1"\" es un archivo ZIP... descomprimiendo e intentando sacar un archivo CDT/TZX
      mkdir -p ${tmptzx}/tzxtmp
      unzip -C "$1" -d ${tmptzx}/tzxtmp
      for i in `ls ${tmptzx}/tzxtmp/*.{tzx,cdt}`;
      do
          playcdt "$i"
      done
      #rm -rf ${tmptzx}/tzxtmp
      exit
   else
      echo ERROR: El archivo \""$1"\" no es un CDT/TZX
   fi
else
   echo ERROR: El archivo \""$1"\" no existe
   exit -1
fi
