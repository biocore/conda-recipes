cd core/
# Remove multithreading for Mac OS
if [ "$(uname)" == "Darwin" ]; then
	sed -i -e "s|ENABLE_MULTITHREAD = -Denablemultithread|#ENABLE_MULTITHREAD = -Denablemultithread|g" Makefile
fi
# Change installation path to $PREFIX
sed -i -e "s|PREFIX = /usr/local|PREFIX = $PREFIX|g" Makefile
make clean
make
make install
