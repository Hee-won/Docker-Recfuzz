#!/bin/bash
git clone https://github.com/Hee-won/Recfuzz.git || exit 1
cd Recfuzz && sudo apt-get -yy install libjson-c-dev libssl-dev libxml2-dev || exit 1
make 
cd ..
chmod 777 -R Recfuzz
cd Recfuzz