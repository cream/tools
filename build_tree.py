import os, sys

from distutils.sysconfig import get_python_lib

SITE_PACKAGES = get_python_lib()
RUN_AGAIN = False

try:
    import cream.dist
except ImportError:
    RUN_AGAIN = True

class TreeError(Exception):
    pass

class SetupData(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return '<SetupData args=%r kwargs=%r>' % (self.args, self.kwargs)

def get_setup_data(filename):
    with open(filename, 'r') as f:
        setuppy = f.read()
    # Replace setup() call
    if not 'setup(' in setuppy:
        raise TreeError('Malformed setup.py (no setup call): %s' % filename)
    setuppy = setuppy.replace('setup(', 'setup_data = yay_setup(')
    sandbox = {'yay_setup': SetupData}
    cwd = os.getcwd()
    os.chdir(os.path.abspath(os.path.dirname(filename)))
    try:
        exec setuppy in sandbox
    except BaseException, e:
        if (isinstance(e, ImportError) and str(e) == 'No module named cream.dist'):
            # Ignore that error. (DIRTY!)
            pass
        else:
            print 'Exception: %r' % e
        return None
    else:
        setup_data = sandbox['setup_data']
        if setup_data.args:
            # A manifest! (O yeah, cream.dist exists)
            setup_data.kwargs = cream.dist.get_pkg_info(*setup_data.args, **setup_data.kwargs)
        return setup_data
    finally:
        os.chdir(cwd)

def get_available_packages(root):
    for dirpath, dirnames, filenames in os.walk(root):
        if 'setup.py' in filenames:
            yield dirpath

def get_package_locations(packages):
    for packagedir in packages:
        setup_data = get_setup_data(os.path.join(packagedir, 'setup.py'))
        if setup_data:
            if 'packages' in setup_data.kwargs:
                # TODO: cream.dist
                package_dir = setup_data.kwargs.get('package_dir', {})
                for packagename in setup_data.kwargs['packages']:
                    directory = os.path.join(packagedir, \
                        package_dir.get(packagename, packagename.replace('.', os.path.sep)))
                    yield (packagename, directory)
            if 'py_modules' in setup_data.kwargs:
                for modulename in setup_data.kwargs['py_modules']:
                    yield (modulename, os.path.join(packagedir, modulename + '.py'))

def build_tree(tree_root, locations):
    tree_root = os.path.abspath(tree_root)
    if not os.path.exists(tree_root):
        os.makedirs(tree_root)
    for name, fs_location in locations:
        fs_location = os.path.abspath(fs_location)
        if os.path.isdir(fs_location):
            # Package.
            tree_location = os.path.join(tree_root, name.replace('.', os.path.sep))
            print 'Installing %s to %s' % (name, tree_location)
            if not os.path.exists(tree_location):
                os.makedirs(tree_location)
            for dirpath, dirnames, filenames in os.walk(fs_location):
                abs_dirpath = os.path.normpath(os.path.join(fs_location, dirpath))
                rel_dirpath = os.path.relpath(dirpath, fs_location)
                for to_filename in filenames:
                    create = os.path.join(tree_location, rel_dirpath, to_filename)
                    if not os.path.islink(create):
                        os.symlink(os.path.join(abs_dirpath, to_filename), create)
                for dirname in dirnames:
                    create = os.path.join(tree_location, rel_dirpath, dirname)
                    if not os.path.exists(create):
                        os.makedirs(create)
        else:
            # Module.
            tree_location = os.path.join(tree_root, name + '.py')
            print 'Installing %s to %s' % (name, tree_location)
            if not os.path.islink(tree_location):
                os.symlink(fs_location, tree_location)

if __name__ == '__main__':
    print 'Usage: build_tree.py [ROOT] (defaults to site-packages)'
    try:
        root = sys.argv[1]
    except IndexError:
        root = SITE_PACKAGES
    build_tree(root, list(get_package_locations(list(get_available_packages('.')))))
    print '--- Done.'
    if RUN_AGAIN:
        print 'Please run build_tree.py again to install modules as well.'
