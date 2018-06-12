# This repository is DEPRECATED. We recommend you submit your recipes to [bioconda](https://bioconda.github.io) or [conda-forge](https://conda-forge.org/)

# `Conda Recipes`
[![Travis Build Status](https://travis-ci.org/biocore/conda-recipes.png?branch=master)](https://travis-ci.org/biocore/conda-recipes)

Conda is a package manager application that quickly installs, runs, and updates packages and their dependencies. It is designed to be Python agnostic and to manage complex dependencies. It can essentially handle any type of packages and their dependencies in an isolated virtual environment.

This repository hosts conda recipes for various biocore packages or dependencies. The idea is to make bioinformatics tools readily installable and host them on [anaconda cloud](http://anaconda.org).

This will make software installation much easier for users with or without much command line experience.

Currently, the packages (and their versions) are built and available on the anaconda organization named [biocore](https://anaconda.org/biocore)

To install a package, you just need to run:

    conda install -c biocore -c bioconda -c conda-forge <package-name>

This installation command tries to install the package from the previous channel; if not found, it then tries to install from the following packages. We order the channels from more specific to more general channels. No endless headache of time-consuming compilation and missing dependecies any more!


## Create a new conda recipe
To add a new package to the pool, you need to create a recipe to tell conda how to build it.

How to create a recipe is documented on [conda's website](http://conda-test.pydata.org/docs/build.html).

You can also borrow from the examples located in this repository: [recipes](https://github.com/biocore/conda-recipes/tree/master/recipes). There are also lots of examples in conda's conda-recipes [repository](https://github.com/conda/conda-recipes/).

## Modify an existing conda recipe
If you modified an existing recipe in this repository and would like to merge it back, you should increment the build number by one in order to trigger a package rebuild. This is not necessary if the package version is changing, and you will need to add the build number section to the `meta.yaml` file if it doesn't already exist.

For example, if the current recipe has this in the `meta.yaml`:

    build:
      number: 1

you should change it to the following after you modify it:

    build:
      number: 2

If there is no such section in `meta.yaml`, the build number defaults to zero. You should set it to 1 after modifying it. Please see the documentation [here](http://conda.pydata.org/docs/building/meta-yaml.html#build-number-and-string)

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

You can find the path to the built package with following commands:

cd <recipe-directory>
    conda build . --output

Now other people can download and install your package (given it is public):

    conda install -c <your-channel> <package-name>

## Contribute your recipes to this repo
We encourage you to add your new recipe into this repo. Each recipe should be in its own directory under [recipes](https://github.com/biocore/conda-recipes/tree/master/recipes). Once you issue a pull request to merge your recipe into this repo, a Travis continuous integration (CI) will run and test your recipe by building the package and uploading it to [biocore](https://anaconda.org/biocore). If the Travis build succeeds, congrats! Your package will be available to download and install from biocore.
