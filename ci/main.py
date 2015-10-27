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
    logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)


def build_upload_recipes(p, channel):
    '''Build & upload recipes recursively in a directory.

    Parameters
    ----------
    p : str
        directory path to the recipes
    channel : str
        the channel where the packages will be uploaded.
    '''
    for root, dirs, files in os.walk(p):
        has_recipe = 'meta.yaml' in files
        if not dirs and has_recipe:
            with open(os.path.join(root, 'meta.yaml')) as f:
                log.info('process {0}.'.format(root))
                meta = yaml.load(f)
                try:
                    build_n = meta['build']['number']
                except KeyError:
                    # if not specified, the build number is 0 by default
                    build_n = 0
                pkg = meta['package']
                name = pkg['name']
                version = pkg['version']
                if check(name, version, build_n, channel):
                    build(name, version, root)
                    if os.environ['TRAVIS_SECURE_ENV_VARS'] == 'true':
                        upload(name, version, channel)
                    else:
                        log.warning('uploading not available in Pull Request.')
                else:
                    log.info('skip building {0}.'.format(root))


def check(name, version, build_n, channel):
    '''Check if we want to build & upload a package.

    It checks package name, package version, and package build number
    sequentially to decide whether to return True or not.

    Parameters
    ----------
    name : str
        package name.
    version : str
        package version.
    build_n : int
        build number
    channel : str
        the channel to check the previous built.

    Returns
    -------
    boolean
        If a previous package in the channel has the same name, the same
        version, and an equal or higher build number, then return False;
        otherwise, return True.
    '''
    cmd = ('conda search --json --override-channels '
           '-c {0} --spec {1}').format(channel, name)
    log.info('check: {0}'.format(cmd))
    out = check_output(cmd, shell=True)
    res = json.loads(out)
    if name not in res:
        return True
    if version != res[name][0]['version']:
        return True
    if build_n > res[name][0]['build_number']:
        return True
    return False


def build(root):
    '''Build a recipe.

    Parameters
    ----------
    root : str
        the directory path for the recipe.
    '''
    # Quote is need in case the root path has spaces in it.
    cmd = 'conda build "{0}"'.format(root)
    log.info('build: {0}'.format(cmd))
    check_call(cmd, shell=True)


def upload(name, version, channel):
    '''Upload a built package.

    Parameters
    ----------
    name : str
        package name.
    version : str
        package version.
    channel : str
        the channel where the package will be uploaded.
    '''
    built_glob = os.path.join(
        config.bldpkgs_dir, '{0}-{1}*.tar.bz2'.format(name, version))
    built = glob.glob(built_glob)[0]
    cmd = 'anaconda -t {token} upload -u {channel} {built}'
    # Do not show decrypted token!
    log.info('upload: {0}'.format(cmd))
    check_call(
        cmd.format(token=os.environ['ANACONDA_TOKEN'],
                   channel=channel,
                   built=built),
        shell=True)


if __name__ == '__main__':
    build_upload_recipes(sys.argv[1], sys.argv[2])
