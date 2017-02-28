make

mkdir -p $PREFIX/bin
mv run_memsat-svm.pl $PREFIX/bin

mkdir -p $PREFIX/share/memsat-svm/
mv * $PREFIX/share/memsat-svm/
ln -s $PREFIX/bin/run_memsat-svm.pl $PREFIX/share/memsat-svm/run_memsat-svm.pl
