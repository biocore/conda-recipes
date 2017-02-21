rm -rf bin/
cd src/
make
make install

mkdir -p $PREFIX/bin
mv ../runpsipred.pl ../bin/* $PREFIX/bin

mkdir -p $PREFIX/share/psipred_4.01/
mv ../data $PREFIX/share/psipred_4.01/
