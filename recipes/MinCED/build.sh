#!/bin/bash

make
mkdir -p "$PREFIX/bin/"
# keep `minced` and `minced.jar` in the same folder
mv minced minced.jar "$PREFIX/bin/"
