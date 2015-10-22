case "${TRAVIS_OS_NAME}" in
    osx)
        os="MacOSX"
        ;;
    linux)
        os="Linux"
        ;;
    *)
        os="Unknown"
esac

MINICONDA_URL="http://repo.continuum.io/miniconda"
MINICONDA_FILE="Miniconda-latest-${os}-x86_64.sh"
wget "${MINICONDA_URL}/${MINICONDA_FILE}"
bash $MINICONDA_FILE -b

export PATH=$HOME/miniconda/bin:$PATH

conda update --yes conda
conda install --yes pip conda-build anaconda-client
