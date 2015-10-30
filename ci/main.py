import os
import sys
import json
import yaml
import glob
import logging
from subprocess import check_call, check_output

from conda_build.config import config


log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)


def build_upload_recipes(p, channel):
    '''Build & upload recipes recursively in a directory.

    Parameters
    ----------
    p : str
        Path to the recipes.
    channel : str
        Anaconda channel where the packages will be uploaded.
    '''
    for root, dirs, files in os.walk(p):
        has_recipe = 'meta.yaml' in files
        if not dirs and has_recipe:
            with open(os.path.join(root, 'meta.yaml')) as f:
                meta = yaml.load(f)
                name = meta['package']['name']
                version = meta['package']['version']
                try:
                    build_number = meta['build']['number']
                except KeyError:
                    # Build number is 0 if not specified
                    build_number = 0
                if is_already_uploaded(name, version, build_number, channel):
                    # Only new packages (either version or build_number)
                    log.info("Skipping package: {0}-{1}".format(name, version))
                    continue
                build(root)
                if os.environ['TRAVIS_SECURE_ENV_VARS'] == 'true':
                    upload(name, version, channel)
                else:
                    log.info("Uploading not available in Pull Requests")


def build(root):
    '''Build a recipe.

    Parameters
    ----------
    root : str
        the directory path for the recipe.
    '''
    # Quote is need in case the root path has spaces in it.
    build_cmd = 'conda build "%s"' % root
    log.info('Building: {0}'.format(build_cmd))
    check_call(build_cmd, shell=True)


def is_already_uploaded(name, version, build_number, channel):
    '''Check if we want to build & upload a package.

    It checks package name, version and build number
    sequentially to decide whether to build and upload it or not.

    Parameters
    ----------
    name : str
        Package name.
    version : str
        Package version.
    build_number : int
        Build number
    channel : str
        Anaconda channel to check the previous build.

    Returns
    -------
    Bool
        If a package in the channel has the same name, the same
        version, and an equal or higher build number, then return
        True; otherwise, return False.

    '''
    check_cmd = ('conda search --json --override-channels '
                 '-c {0} --spec {1}={2}').format(
                     channel, name, version)
    log.info('Checking: {0}'.format(check_cmd))
    out = check_output(check_cmd, shell=True)
    res = json.loads(out)
    return all((name in res,
                res[name][0]['version'] == version,
                res[name][0]['build_number'] >= build_number))


def upload(name, version, channel):
    '''Upload a built package.

    Parameters
    ----------
    name : str
        Package name.
    version : str
        Package version.
    channel : str
        Channel where the package will be uploaded.
    '''
    built_glob = os.path.join(
        config.bldpkgs_dir,
        '{0}-{1}*.tar.bz2'.format(name, version))
    built = glob.glob(built_glob)[0]
    upload_cmd = 'anaconda -t {token} upload -u {channel} {built}'
    # Do not show decrypted token!
    log.info('Uploading: {0}'.format(upload_cmd))
    check_call(
        upload_cmd.format(
            token=os.environ['ANACONDA_TOKEN'],
            built=built,
            channel=channel),
        shell=True)


if __name__ == '__main__':
    build_upload_recipes(sys.argv[1], sys.argv[2])
