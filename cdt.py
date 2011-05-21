#! /usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
import tempfile
import tarfile
import os
import sys
import shutil
import dulwich.repo
import dulwich.client

IGNORED_FILES = [
    '.git',
    '.gitignore'
]

def git_clone(remote, local):
    
    client, host_path = dulwich.client.get_transport_and_path(remote)

    if not os.path.exists(local):
        os.mkdir(local)

    r = dulwich.repo.Repo.init(local)

    remote_refs = client.fetch(host_path, r,
        determine_wants=r.object_store.determine_wants_all,
        progress=sys.stdout.write)

    r["HEAD"] = remote_refs["HEAD"]


class CreamDevelopmentTool(object):
    
    def __init__(self):

        parser = optparse.OptionParser()
        options, args = parser.parse_args()

        command = getattr(self, args[0])
        command(*args[1:])
        
    
    def release(self, target, repo, version):

        print " » Cloning repository…"
        tmp = tempfile.mkdtemp(prefix='cdt-')
        git_clone(repo, tmp)
        
        print " » Checking out working directory…"
        cwd = os.getcwd()
        os.chdir(tmp)
        os.system('git checkout master')
        os.chdir(cwd)

        print " » Removing files related to the repository…"
        for f in IGNORED_FILES:
            print "   » Removing '{0}'…".format(f)
            if os.path.isdir(os.path.join(tmp, f)):
                shutil.rmtree(os.path.join(tmp, f))
            elif os.path.isfile(os.path.join(tmp, f)):
                os.remove(os.path.join(tmp, f))

        print " » Creating the tarball…"
        tarball_name = '{0}-{1}.tar.bz2'.format(target, version)
        tarball_path = os.path.join('/tmp', tarball_name)
        tarball = tarfile.TarFile.open(tarball_path, 'w:bz2')
        tarball.add(tmp, arcname='{0}-{1}'.format(target, version))
        tarball.close()
        
        print " » Removing temporary files…"
        shutil.rmtree(tmp)
    
        print " → You may find the tarball in '{0}'…".format(tarball_path)


if __name__ == '__main__':
    CreamDevelopmentTool()
