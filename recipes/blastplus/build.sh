#!/bin/bash

mkdir -p "$PREFIX/bin"

cd $SRC_DIR
ls -alh

mv -v $SRC_DIR/bin/* $PREFIX/bin
