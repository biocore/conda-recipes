#!/bin/bash

case "$(uname)" in
    Linux)
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
        ;;
    Darwin)
        cd src
        ./install-boost &> /dev/null
        #sed -i "" "s/-march=native/ /g" Makefile
        make
        mkdir -p $PREFIX/bin
        cp ../bin/diamond $PREFIX/bin
        ;;
esac
