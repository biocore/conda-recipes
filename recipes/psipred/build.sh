rm -rf bin/
mkdir bin/ -p
cd src/
make
make install

mkdir -p $PREFIX/bin
chmod u+x ../runpsipred.pl
mv ../runpsipred.pl ../bin/* $PREFIX/bin

mkdir -p $PREFIX/share/psipred_4.01/
mv ../data $PREFIX/share/psipred_4.01/
