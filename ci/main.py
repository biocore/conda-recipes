import os
import sys
import json
import yaml
import glob
import logging
from subprocess import run, PIPE

from conda_build.config import Config


config = Config()

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
                log.info("Checking {}".format(root))
                meta = yaml.load(f)
                name = meta['package']['name']
                version = meta['package']['version']
                try:
                    build_number = meta['build']['number']
                except KeyError:
                    # Build number is 0 if not specified
                    build_number = 0
                if is_not_uploaded(name, version, build_number, channel):
                    build(root)
                    if os.environ['TRAVIS_SECURE_ENV_VARS'] == 'true':
                        upload(name, version, channel)
                    else:
                        log.info("Uploading not available in Pull Requests")
                else:
                    # Only new packages (either version or build_number)
                    log.info("Skipping package: {0}-{1}-{2}".format(
                        name, version, build_number))


def build(root):
    '''Build a recipe.

    Parameters
    ----------
    root : str
        the directory path for the recipe.
    '''
    # Quote is need in case the root path has spaces in it.
    build_cmd = 'conda build --dirty "%s"' % root
    log.info('Building: {0}'.format(build_cmd))
    proc = run(build_cmd, shell=True)
    log.info(proc)


def is_not_uploaded(name, version, build_number, channel):
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
        False; otherwise, return True.

    '''
    check_cmd = ('conda search --json --override-channels '
                 '-c {0} {1}').format(
                     channel, name)
    log.info('Checking: {0}'.format(check_cmd))
    proc = run(check_cmd, shell=True, stdout=PIPE)
    log.info(proc)
    res = json.loads(proc.stdout.decode('utf-8'))

    if name not in res:
        return True
    pkg = res[name]
    if version not in [i['version'] for i in pkg]:
        return True
    if build_number > max(
            i['build_number'] for i in pkg if i['version'] == version):
        return True
    return False


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
    upload_cmd = 'anaconda -t {token} upload -u %s %s' % (channel, built)
    # Do not show decrypted token!
    log.info('Uploading: {0}'.format(upload_cmd))
    proc = run(
        upload_cmd.format(token=os.environ['ANACONDA_TOKEN']),
        shell=True)
    log.info(proc)


if __name__ == '__main__':
    build_upload_recipes(sys.argv[1], sys.argv[2])
