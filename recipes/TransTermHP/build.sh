make clean transterm 2ndscore
mv transterm 2ndscore $PREFIX/bin
mkdir -p $PREFIX/share/transtermhp/
mv expterm.dat $PREFIX/share/transtermhp/
# set environment variable of $TRANSTERMHP  when activating environment
mkdir -p $PREFIX/etc/conda/activate.d/
echo "export TRANSTERMHP=$PREFIX/share/transtermhp/expterm.dat" > $PREFIX/etc/conda/activate.d/transtermhp.sh
mkdir -p $PREFIX/etc/conda/deactivate.d/
echo "unset TRANSTERMHP" > $PREFIX/etc/conda/deactivate.d/transtermhp.sh
