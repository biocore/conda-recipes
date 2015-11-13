#!/bin/bash

conda install -c menpo boost

mkdir build
cd build

CMAKE_ARCH="-m"$ARCH
INCLUDE_PATH=${PREFIX}/include
LIBRARY_PATH=${PREFIX}/lib

export LDFLAGS="-L${LIBRARY_PATH} $LDFLAGS"

cmake -LAH .. \
-DCMAKE_PREFIX_PATH=$PREFIX \
-DCMAKE_INSTALL_PREFIX=$PREFIX \
-DBOOST_ROOT=$PREFIX \
-DBOOST_INCLUDEDIR="${INCLUDE_PATH}" \
-DBOOST_LIBRARYDIR="${LIBRARY_PATH}" \

cmake --build . --config Release --target install
