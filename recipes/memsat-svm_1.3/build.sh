sed -i "s|my \$ncbidir = '';|my \$ncbidir = '/opt/anaconda1anaconda2anaconda3/bin/';|" run_memsat-svm.pl
sed -i "s|my \$mem_dir = '';|my \$mem_dir = '/opt/anaconda1anaconda2anaconda3/share/memsat-svm/';|" run_memsat-svm.pl
sed -i "s|use lib 'lib';|use lib '/opt/anaconda1anaconda2anaconda3/share/memsat-svm/lib/';|" run_memsat-svm.pl

make

mkdir -p $PREFIX/bin
mv run_memsat-svm.pl $PREFIX/bin

mkdir -p $PREFIX/share/memsat-svm/
mv * $PREFIX/share/memsat-svm/
ln -s $PREFIX/bin/run_memsat-svm.pl $PREFIX/share/memsat-svm/run_memsat-svm.pl
