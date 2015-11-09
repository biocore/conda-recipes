#!/bin/bash

cd src
./install-boost &> /dev/null
#sed -i "" "s/-march=native/ /g" Makefile
make
cp ../bin/diamond "$PREFIX/bin"
