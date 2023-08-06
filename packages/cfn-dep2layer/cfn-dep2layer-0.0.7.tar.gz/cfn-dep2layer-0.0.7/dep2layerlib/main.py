import cfnyaml
import os
import tempfile
import shutil
import downloaders


DEFAULT_TEMPLATE = 'template.yaml'
DEFAULT_OUT_TEMPLATE = '.dep2layer-template.yaml'
DEFAULT_CACHE = '.dep2layer'
LAYER_PREFIX = 'Dep2layer'


def createlayer(template, layername, resource, downloader, cachedir):
  zippath = os.path.join(cachedir, '{}-{}.zip'.format(downloader.prefix, downloader.gethash()[:7]))
  layername = 'Dep2layer{}H{}'.format(downloader.prefix, downloader.gethash()[:7])
  if not os.path.isfile(zippath):
    print('Download dependencies...')
    with tempfile.TemporaryDirectory(dir='/tmp') as tempdir:
      print('Using temp dir: {}'.format(tempdir))
      
      if not downloader.package(tempdir):
        print('Download faild.')
        return False
        
      with open(os.path.join(tempdir, '.dep2layer/hash.txt'), 'w') as f:
        f.write(downloader.gethash())
      
      shutil.make_archive(zippath[:-4], 'zip', tempdir)
      print('Created content zip: ')
  else:
    print('Zip already exist: {}'.format(zippath))
    
  template['Resources'][layername] = {
      'Type': 'AWS::Serverless::LayerVersion',
      'Properties': {
        'Layername': 'dep2layer-{}-{}'.format(downloader.prefix, downloader.gethash()[:7]),
        'Description': 'Create by dep2layer, contain packages:\n{}'.format('|'.join(downloader.getdeplist())),
        'ContentUri': zippath,
        'CompatibleRuntimes' : [resource['Properties']['Runtime']],
        'RetentionPolicy': 'Delete'
      }
  }
  
  return True


def work(templatepath=None, cachedir=None, outtemplatepath=None):
  
  templatepath = os.path.abspath(DEFAULT_TEMPLATE if templatepath is None else templatepath)
  basedir = os.path.abspath(os.path.join(templatepath, '..'))
  cachedir = os.path.abspath(os.path.join(basedir, DEFAULT_CACHE) if cachedir is None else cachedir)
  outtemplatepath = os.path.abspath(os.path.join(basedir, DEFAULT_OUT_TEMPLATE) if outtemplatepath is None else outtemplatepath)
  
  try:
    with open(templatepath) as f:
      template = cfnyaml.load(f)
  except Exception as e:
    print('Error when load template file: {}\n{}'.format(templatepath, e))
    exit(1)
    
  try:
    os.makedirs(cachedir, exist_ok=True)
  except Exception as e:
    print('Error when create cache dir: {}\n{}'.format(basedir, e))
    exit(1)
    
  for key, resource in list(template['Resources'].items()):
    if resource['Type'] == 'AWS::Serverless::Function':
      if resource['Properties']['Runtime'] in downloaders.cls:
        print('===== Lambda [{}] {} ====='.format(key, resource['Properties']['Runtime']))
        downloader = downloaders.cls[resource['Properties']['Runtime']](resource, basedir)
        
        layername = '{}{}H{}'.format(DEFAULT_CACHE, downloader.prefix, downloader.gethash()[:7])
        if layername not in template:
          if not createlayer(template, layername, resource, downloader, cachedir):
            continue
            
        if 'Layers' not in resource['Properties']:
          resource['Properties']['Layers'] = []
        for ref in resource['Properties']['Layers']:
          if ref.logicalName.find(LAYER_PREFIX) == 0:
            ref.logicalName = layername
            break
        else:
          resource['Properties']['Layers'].append(cfnyaml.Ref(layername))

    
  try:
    with open(outtemplatepath, 'w') as f:
      f.write(cfnyaml.dump(template))
  except Exception as e:
    print('Error when create out template file: {}\n{}'.format(outtemplatepath, e))
    exit(1)
    
def clear():
  pass