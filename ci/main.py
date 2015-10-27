import os
import sys
import json
import yaml
import glob
from subprocess import check_call, check_output, CalledProcessError

from conda_build.config import config


CHANNEL = 'https://conda.anaconda.org/biocore'


def build_upload_recipes(p):
    for root, dirs, files in os.walk(p):
        has_recipe = 'meta.yaml' in files
        if not dirs and has_recipe:
            with open(os.path.join(root, 'meta.yaml')) as f:
                pkg = yaml.load(f)['package']
                name = pkg['name']
                version = pkg['version']
                build_upload(name, version, root)


def build_upload(name, version, root):
    print("Building package: {0}-{1}".format(name, version))
    # Quote is need in case the root path has spaces in it.
    build_cmd = 'conda build "%s"' % root
    print('BUILDING COMMAND: {0}'.format(build_cmd))
    check_call(build_cmd, shell=True)

    check_cmd = ('conda search --json --override-channels '
                 '-c {0} --spec {1}={2}').format(
                     CHANNEL, name, version)
    print('CHECKING COMMAND: {0}'.format(check_cmd))
    try:
        out = check_output(check_cmd, shell=True)
    except CalledProcessError as e:
        # This built version does not exist in the channel
        out = e.output
    res = json.loads(out)
    if name not in res:
        built_glob = os.path.join(
            config.bldpkgs_dir,
            '{0}-{1}*.tar.bz2'.format(name, version))
        built = glob.glob(built_glob)[0]
        upload_cmd = 'anaconda -t {token} upload -u biocore {built}'
        # Do not show decrypted token!
        print('UPLOADING COMMAND: {0}'.format(upload_cmd))
        check_call(
            upload_cmd.format(
                token=os.environ['ANACONDA_TOKEN'], built=built),
            shell=True)


if __name__ == '__main__':
    build_upload_recipes(sys.argv[1])
