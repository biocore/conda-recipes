import sys
import yaml
import glob
from os import walk, environ
from os.path import join
from subprocess import check_call, CalledProcessError
from conda_build.config import config


CHANNEL = 'https://conda.anaconda.org/biocore'


def build_upload_recipes(p):
    for root, dirs, files in walk(p):
        has_recipe = 'meta.yaml' in files
        if not dirs and has_recipe:
            with open(join(root, 'meta.yaml')) as f:
                pkg = yaml.load(f)['package']
                name = pkg['name']
                version = pkg['version']
                build_upload(name, version, root)


def build_upload(name, version, root):
    print("Building package: {0}-{1}".format(name, version))
    # quote is need in case the root path
    # has space in it.
    build_cmd = 'conda build "%s"' % root
    print('BUILDING COMMAND: {0}'.format(build_cmd))
    check_call(build_cmd, shell=True)

    check_cmd = ('conda search --json --override-channels '
                 '-c {0} --spec {1}={2}').format(
                     CHANNEL, name, version)
    print('CHECKING COMMAND: {0}'.format(check_cmd))
    try:
        check_call(check_cmd, shell=True)
    except CalledProcessError:
        # this built does not exist in the channel
        built_glob = join(
            config.bldpkgs_dir,
            '{0}-{1}*.tar.bz2'.format(name, version))
        built = glob.glob(built_glob)[0]
        upload_cmd = 'anaconda -t {token} upload -u biocore {built}'
        # do not show decrypted token
        print('UPLOADING COMMAND: {0}'.format(upload_cmd))
        check_call(
            upload_cmd.format(
                token=environ['ANACONDA_TOKEN'], built=built),
            shell=True)


if __name__ == '__main__':
    build_upload_recipes(sys.argv[1])
