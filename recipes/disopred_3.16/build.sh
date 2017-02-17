sed -i "s|my $NCBI_DIR = \"\";|my \$NCBI_DIR = '/opt/anaconda1anaconda2anaconda3/bin/';|" run_disopred.pl
sed -i "s|my \$EXE_DIR = abs_path(join '\/', \$dir, \"bin\");|my \$EXE_DIR = '/opt/anaconda1anaconda2anaconda3/bin/';|" run_disopred.pl
sed -i "s|my \$DATA_DIR = abs_path(join '\/', \$dir,\"data\");|my \$DATA_DIR = '/opt/anaconda1anaconda2anaconda3/share/disopred_3.16/data/';|" run_disopred.pl
sed -i "s|\$ENV{DSO_LIB_PATH} = join '\/', abs_path(\$dir), \"dso_lib\/\"|\$ENV{DSO_LIB_PATH} = '/opt/anaconda1anaconda2anaconda3/share/disopred_3.16/dso_lib/';|" run_disopred.pl
rm -rf bin/
cd src/
make
make install

mkdir -p $PREFIX/bin
mv ../run_disopred.pl ../bin/* $PREFIX/bin

mkdir -p $PREFIX/share/disopred_3.16/
mv ../data ../dso_lib $PREFIX/share/disopred_3.16/