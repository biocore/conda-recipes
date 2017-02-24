rm -rf bin/
cd src/
make
make install

mkdir -p $PREFIX/bin
mv ../run_disopred.pl ../bin/* $PREFIX/bin

mkdir -p $PREFIX/share/disopred_3.16/
mv ../data ../dso_lib $PREFIX/share/disopred_3.16/