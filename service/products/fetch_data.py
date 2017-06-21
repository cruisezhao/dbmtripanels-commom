"""

software: software data load and check module.

fetch_data.py: fetch software data from extract zip file.

"""
import os
# import json
# import urllib.parse as urlparse
from schema import Schema

from common.service.products.load_utils import extract_file
from common.service.products.load_utils import load_from_dir
from common.service.products.exceptions import SoftwareLoadError
from common.service.products.settings import map_names
from common.service.products.settings import product_schema, app_schema, vm_schema, bare_schema
from common.service.products.settings import _DATA_CHECK


def fetch(archive_path, target_dir=None, drop_dir=False):
    """ 
    @param archive_path: zip file path name
    @param target_dir:  extract tartget path 
    @param drop_dir:  is delete target_dir after fetch software data?
    """
    try:  
        # Extract files from archive_path
        source = extract_file(archive_path, target_dir, drop_dir)
        product = load_product(source)
        
        product_dir_name = os.path.splitext(os.path.split(archive_path)[1])[0]
        assert (product_dir_name == product["product_name"])
        
        product_type = product["product_type"]
        
        product_app = product_load_functions[product_type](source)
        
        return (product_app, product)
  
    except SoftwareLoadError as ex:
        raise Exception(ex)


def load_app_product(source_directory):
    ''' load app product data from app_product.yaml
    '''
    template_file = 'product-app.yaml'
    
    app_product = load_data(source_directory, template_file, app_schema)
    app_product["product_pic"] = os.path.basename(source_directory) + "/" +  \
                                  app_product["product_pic"]
    app_product["product_img"] = os.path.basename(source_directory) + "/" +  \
                                  app_product["product_img"]
    return app_product
   
def load_vm_product(source_directory):
    ''' load vm product data from vm_product.yaml
    '''
    template_file = 'product-vm.yaml'
            
    return load_data(source_directory, template_file, vm_schema)

def load_bare_product(source_directory):
    ''' load bare product data from bare_product.yaml
    '''
    template_file = 'product-bare.yaml'
            
    return load_data(source_directory, template_file, bare_schema)


def load_product(source_directory):
    ''' load products data from product.yaml
    '''
    template_file = 'product.yaml'
            
    return load_data(source_directory, template_file, product_schema)

def load_data(source_directory, template_file, schema_dict):
    ''' load data from yaml template file
    '''
    data = load_from_dir(source_directory, template_file)
    
    if _DATA_CHECK:
        data = Schema(schema_dict).validate(data)
    
    return data


product_load_functions = {
    map_names['product_types']['APP'] : load_app_product,
    map_names['product_types']['VM'] : load_vm_product,
    map_names['product_types']['Bare'] : load_bare_product,
}

            
if __name__ == '__main__':
    
    try:
        archive_path = "packages/archive/ecwid.zip"
        target_dir = "packages/"
        sf = fetch(archive_path, target_dir)
        print(sf[0])
        print(sf[1])    

    except Exception as ex:
        print(ex)



        
    
    
