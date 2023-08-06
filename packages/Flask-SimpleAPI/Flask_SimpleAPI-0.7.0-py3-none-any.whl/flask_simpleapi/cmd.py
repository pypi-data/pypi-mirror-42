import shutil
import os
import sys


def create_app():
    api_name = sys.argv[1]
    pkg_path = os.path.dirname(__file__)

    src = os.path.join(pkg_path, 'project_template')
    dst = api_name
    symlinks = False
    ignore = None

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
