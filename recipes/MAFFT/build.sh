cd core/
eval "sed -ie s/PREFIX = \/usr\/local/PREFIX/g = $PREFIX/" Makefile
make clean
make
make install