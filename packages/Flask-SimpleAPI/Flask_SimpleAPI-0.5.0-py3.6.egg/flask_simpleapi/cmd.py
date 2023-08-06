from os.path import dirname, join

import shutil
import os


def create_app():
    pkg_path = dirname(__file__)

    src = join(pkg_path, 'project_template')
    dst = '.'
    symlinks = False
    ignore = None

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

