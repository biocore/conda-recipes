#!/bin/bash

mkdir -p "$PREFIX/bin"

if [ $TRAVIS_OS_NAME == linux ]
then 
	wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.31/ncbi-blast-2.2.31+-x64-linux.tar.gz
	tar -xvf ncbi-blast-2.2.31+-x64-linux.tar.gz
	cp ncbi-blast-2.2.31+/bin $PREFIX/bin
elif [ $TRAVIS_OS_NAME == mac ]
then
	curl -O ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.31/ncbi-blast-2.2.31+-universal-macosx.tar.gz 
	tar -xvf ncbi-blast-2.2.31+-universal-macosx.tar.gz
	cp ncbi-blast-2.2.31+/bin $PREFIX/bin
	curl asdf
else
	echo "TRAVIS_OS_NAME is not 'linux' or 'mac'. It is set to:" 
	echo $TRAVIS_OS_NAME
fi



