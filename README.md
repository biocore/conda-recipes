# Conda Recipes
[![Travis Build Status](https://travis-ci.org/RNAer/conda-recipes.png?branch=master)](https://travis-ci.org/RNAer/conda-recipes)

Conda is a package manager application that quickly installs, runs, and updates packages and their dependencies.

This repository hosts conda recipes for various biocore packages or dependencies. The idea is to the widely used bioinformatic tools readily installable and host them on [anaconda cloud](http://anaconda.org).

This will make the software installation much easier for users who do not have much command line experience.

Currently, the following packages (and their versions) are built and available on anaconda organization named [biocore](https://anaconda.org/biocore):

HMMER: [![Binstar Badge](https://anaconda.org/biocore/hmmer/badges/version.svg)](https://anaconda.org/biocore/hmmer)

Infernal: [![Binstar Badge](https://anaconda.org/biocore/infernal/badges/version.svg)](https://anaconda.org/biocore/infernal)

Prodigal: [![Binstar Badge](https://anaconda.org/biocore/prodigal/badges/version.svg)](https://anaconda.org/biocore/prodigal)

To install the software, you just need to run:

    conda install -c https://anaconda.org/biocore <package-name>

No endless headache of time-consuming compilation and missing dependecies any more!


## Create a new conda recipe
To add a new piece of software to the pool, you need to create a recipe to tell conda how to build it.

How to create a recipe is documented on [conda website](http://conda-test.pydata.org/docs/build.html).

You can also borrow from the examples located in this repository: [recipes](https://github.com/biocore/conda-recipes/tree/master/recipes)


## Build a conda package
You need to install the following mandatory toolset before building a package.

    conda install anaconda-client
    conda install conda-build

Once you install the toolset and create your recipe, you can build the package with the following command:

    conda build <recipe-directory>

Please see the conda [build docs](http://conda.pydata.org/docs/building/build.html) for further information.

## Upload a conda package
To upload your built package to anaconda for others to download and install, you need to create an account [here](https://anaconda.org).

You will need to login with your account credentials you just created:

    anaconda login

And use this command to upload:

    anaconda upload <path-to-your-conda-package.tar.bz2>

You can find the path of the built package with following commands:

    cd <recipe-directory>
    conda build . --output

Now other people can download and install your package (given it is public):

    conda install -c <your-channel> <package-name>

## Contribute your recipes to this repo
You can add your new recipe into this repo. Each recipe needs to be in its own directory under [recipes](https://github.com/biocore/conda-recipes/tree/master/recipes). Once your issue a pull request to merge your recipe into this repo, a Travis continuous integration (CI) will run and test your recipe by building the package and uploading it to [biocore](https://anaconda.org/biocore). If Travis CI is passed, congrats! Your package will be available to download from biocore.
