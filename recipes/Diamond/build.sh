#!/bin/bash

conda install boost

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$PREFIX/bin ..
make install

