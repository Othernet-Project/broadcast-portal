import shutil
from os.path import abspath, join, exists

from . import Command

from ..util.skinning import skin_dir


class CustomSkin(Command):
    name = 'custom-skin'
    help = 'create custom skin directory'

    def add_args(self):
        self.group.add_argument('output', metavar='PATH', help='output path')

    def run(self, args):
        self.exts.skindir = abspath(join(self.exts.root, 'skins'))
        output_path = args.output
        if exists(output_path):
            print("ERROR: '{}' already exists".format(args.custom_skin))
            self.quit(1)
        shutil.copytree(skin_dir(), output_path)
        print("Created skin in '{}'".format(output_path))
        self.quit(0)
