import subprocess
import hashlib
import os

class PackagerBase:
  image = None
  rundir = None # Need "run.sh" in this dir
  prefix = None
  
  def __init__(self, resource, basedir):
    self.resource = resource
    self.basedir = basedir
    self.hash = None
  
  def getdeplist(self):
    pass
    
  def gethash(self):
    if self.hash is None:
      sha = hashlib.sha256()
      sha.update('|'.join(self.getdeplist()).encode('utf8'))
      self.hash = sha.hexdigest()
    return self.hash
  
  def package(self, tmpdir):
    print('=========', os.path.realpath(__file__)))
    args = [ 'docker', 'run', '--rm', '--entrypoint', '', \
      '-v', '{}:/var/task/packager:ro'.format(os.path.abspath(self.rundir)), \
      '-v', '{}:/var/task/src:ro'.format(os.path.join(self.basedir, self.resource['Properties']['CodeUri'])), \
      '-v', '{}:/tmp'.format(tmpdir), \
      self.image, 'bash', '/var/task/packager/run.sh']
    
    print(args)
    proc = subprocess.Popen(args)
    proc.wait()
    
    return proc.returncode == 0

class Python37Packager(PackagerBase):
  image = 'lambci/lambda:python3.7'
  rundir = 'python3'
  prefix = 'Python37'
  
  def getdeplist(self):
    requirementpath = os.path.join(self.basedir, self.resource['Properties']['CodeUri'], 'requirements.txt')
    return [i.strip() for i in open(requirementpath).readlines()]

cls = {
  'python3.7': Python37Packager
}