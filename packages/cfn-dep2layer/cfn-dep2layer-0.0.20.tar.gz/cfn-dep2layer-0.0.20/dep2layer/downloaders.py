import subprocess
import hashlib
import os
import shutil


class PackagerBase:
  image = None
  _rundir = None # Need "run.sh" in this dir
  prefix = None
  depfiles = []
  
  def __init__(self, resource, basedir):
    self.resource = resource
    self.basedir = basedir
    self.hash = None
    self.depfiles = []
    
  @classmethod
  def isdepfilesexists(cls, resource, basedir):
    for f in cls.depfiles:
      if not os.path.isfile(os.path.join(self.basedir, self.resource['Properties']['CodeUri'], f)):
        return False
    return True
    
  def getdeplist(self):
    pass
    
  @property
  def rundir(self):
    return os.path.abspath(os.path.join(os.path.realpath(__file__), '..', self._rundir))
    
  
    
  def gethash(self):
    if self.hash is None:
      sha = hashlib.sha256()
      sha.update('|'.join(self.getdeplist()).encode('utf8'))
      self.hash = sha.hexdigest()
    return self.hash
  
  def package(self, tempdir):
    print('=========', __file__, os.path.realpath(__file__))
    
    # Copy code to temp dir to share with Docker VM
    runtempdir = os.path.join(tempdir, '.packager')
    shutil.copytree(self.rundir, runtempdir)
    
    args = [ 'docker', 'run', '--rm', '--entrypoint', '', \
      '-v', '{}:/var/task/packager:ro'.format(runtempdir), \
      '-v', '{}:/var/task/src:ro'.format(os.path.join(self.basedir, self.resource['Properties']['CodeUri'])), \
      '-v', '{}:/tmp'.format(tempdir), \
      self.image, 'bash', '/var/task/packager/run.sh']
    
    print(args)
    proc = subprocess.Popen(args)
    proc.wait()
    
    shutil.rmtree(runtempdir)
    
    return proc.returncode == 0

class Python37Packager(PackagerBase):
  image = 'lambci/lambda:python3.7'
  _rundir = 'python3'
  prefix = 'Python37'
  depfiles = ['requirements.txt']
  
  def getdeplist(self):
    requirementpath = os.path.join(self.basedir, self.resource['Properties']['CodeUri'], 'requirements.txt')
    return [i.strip() for i in open(requirementpath).readlines()]

class Python36Packager(Python37Packager):
  image = 'lambci/lambda:python3.6'
  prefix = 'Python36'

cls = {
  'python3.7': Python37Packager,
  'python3.6': Python36Packager
}