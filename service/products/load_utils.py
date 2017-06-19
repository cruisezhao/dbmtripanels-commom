"""

software: software data load and check module.

load_utils.py: extract zip file and load yaml file module.

"""
import os
import shutil
import sys
import tempfile
import zipfile

import six
import yaml

import common.service.products.exceptions as e

def extract_file(archive_path, target_dir=None, drop_dir=False):
    """
    """
    software_name = os.path.splitext(os.path.split(archive_path)[1])[0]
    
    if not os.path.isfile(archive_path):
        raise e.SoftwareLoadError('Unable to find software archive file')
    
    created = False
    if not target_dir:
        target_dir = tempfile.mkdtemp()
        created = True
    
    elif not os.path.exists(target_dir):
        os.makedirs(target_dir)
        created = True
    
    software_dir = os.path.join(target_dir, software_name)
    if os.path.exists(software_dir):
        raise e.SoftwareLoadError('Target directory is not empty')
        
    try:
        if not zipfile.is_zipfile(archive_path):
            raise e.SoftwareLoadError("Uploaded file {0} is not a "
                                       "zip archive".format(archive_path))
            
        package = zipfile.ZipFile(archive_path)
        package.extractall(path = target_dir)
        
        
        
        return software_dir
        
    except ValueError as err:
        raise e.SoftwareLoadError("Couldn't load package from file: "
                                 "{0}".format(err))
    finally:
        if drop_dir:
            if created:
                shutil.rmtree(target_dir)
            else:
                for f in os.listdir(target_dir):
                    os.unlink(os.path.join(target_dir, f))

def load_from_dir(source_directory, filename='software.yaml'):
    """
    """
    if not os.path.isdir(source_directory) or not os.path.exists(
            source_directory):
        raise e.SoftwareLoadError('Invalid package directory')
    
    full_path = os.path.join(source_directory, filename)
    
    if not os.path.isfile(full_path):
        raise e.SoftwareLoadError('Unable to find {0}'.format(filename))
    try:
        with open(full_path) as stream:
            content = yaml.safe_load(stream)
            
    except Exception as ex:
        trace = sys.exc_info()[2]
        six.reraise(
            e.SoftwareLoadError,
            e.SoftwareLoadError("Unable to load due to '{0}'".format(ex)),
            trace)
    else:
        return content

if __name__ == '__main__':
    import os.path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_directory = os.path.join(base_dir,'products\software-dir\magento')
    print(os.path.isdir(source_directory))
    content = load_from_dir(source_directory)
    print(content)
    #extract_file
    archive_path = os.path.join(base_dir, 'products\clusters-apps\woocommmerce.zip')
    target_dir = os.path.join(base_dir, 'products\software-dir')
    extract_file(archive_path, target_dir)