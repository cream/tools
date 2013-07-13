import os
import sys


class InstallHandler(object):

    name = None
    dirs = {}
    files = {}

    def __init__(self, src_base_path, dest_base_path):
        self.src_base_path = src_base_path
        self.dest_base_path = dest_base_path

    def get_files(self):

        f = []
        for src_name in self.dirs.keys():
            dest_name = self.dirs[src_name]
            path = os.path.join(self.src_base_path, src_name)
            for dirpath, dirnames, filenames in os.walk(path):
                dirpath = os.path.relpath(dirpath, path)
                for filename in filenames:
                    src = os.path.join(self.src_base_path, src_name, dirpath, filename)
                    dest = os.path.join(self.dest_base_path, dest_name, dirpath, filename)
                    f.append((src, dest))

        for src_name in self.files.keys():
            dest_name = self.files[src_name]
            src = os.path.join(self.src_base_path, src_name)
            dest = os.path.join(self.dest_base_path, dest_name)
            f.append((src, dest))

        return f


    def install(self):

        for src, dest in self.get_files():
            dest_dirname = os.path.dirname(dest)
            if not os.path.exists(dest_dirname):
                os.makedirs(dest_dirname)
            print 'Installing {} to {}'.format(src, dest)
            os.symlink(src, dest)


class GpyconfInstallHandler(InstallHandler):
    name = 'gpyconf'
    dirs = {
        'gpyconf/': 'gpyconf/'
    }

class PythonCreamInstallHandler(InstallHandler):
    name = 'python-cream'
    dirs = {
        'cream/': 'cream/'
    }

class MelangeInstallHandler(InstallHandler):
    name = 'melange'
    dirs = {
        'src/melange/': 'cream/melange/',
        'data/': 'data/cream-melange'
    }
    files = {
        'src/melange.py': 'melange.py'
    }

class MelangeWidgetsInstallHandler(InstallHandler):
    name = 'melange-widgets'
    dirs = {
        'src/': 'data/cream-melange/widgets'
    }


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        src_path = sys.argv[1]
        target_path = sys.argv[2]
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        elif os.listdir(target_path):
            print 'Install directory {} not empty. Exiting...'.format(target_path)
            sys.exit(1)

        print 'Installing to {}'.format(target_path)

        for klass in InstallHandler.__subclasses__():
            src = os.path.join(src_path, klass.name)
            handler = klass(src, target_path)

            print 'Installing {}'.format(klass.name)
            handler.install()
    else:
        print 'Usage python build_tree.py src target'
