cd core/
sed -i -e "s|PREFIX = /usr/local|PREFIX = $PREFIX|g" Makefile
make clean
make
make install
