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
import common.service.products.exceptions as e
from common.service.products.settings import software_schema, products_schema
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
        software = load_software(source)
        
        software_name = os.path.splitext(os.path.split(archive_path)[1])[0]
        software["software_pic"] = software_name + "/" + software["software_pic"] # os.path.join(software_name, software["software_logo"])
        software["software_img"] = software_name + "/" + software["software_img"]   # os.path.join(software_name, software["software_img"])
        
        products = load_products(source)
        return(software, products)    
    except e.SoftwareLoadError as ex:
        raise Exception(ex)


def load_software(source_directory):
    ''' load software data from software.yaml
    '''
    # add data valid check here
    software = load_from_dir(source_directory, 'software.yaml')
    
    if _DATA_CHECK:
        software = Schema(software_schema).validate(software)
    
    return software

def load_products(source_directory):
    ''' load products data from products.yaml
    '''
    # add data valid check here
    products_dir = os.path.join(source_directory, 'products')
    products = load_from_dir(products_dir, 'products.yaml')
    
    if _DATA_CHECK:
        products = Schema(products_schema).validate(products)
        
    return products
   
            
if __name__ == '__main__':
    
    try:
        archive_path = "clusters-apps/woocommmerce.zip"
        target_dir = "software-dir/"
        # sf = fetch(archive_path, target_dir)
        # print(sf[0])
        # print(sf[1])    
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        source_directory = os.path.join(base_dir,'products\software-dir\magento')
        software = load_software(source_directory)
        print(software)
        products = load_products(source_directory)
        print(products)
        # software_img_root = "http://portal.databasemart.net/software-img/"
        
        # logo_url = urlparse.urljoin(software_img_root, sf[0]["software_logo"])
        # print(logo_url)
    except Exception as ex:
        print(ex)

    #fetch
    archive_path = os.path.join(base_dir, 'products\clusters-apps\woocommmerce.zip')
    target_dir = os.path.join(base_dir, 'products\software-dir')
    a,b=fetch(archive_path, target_dir)
    print(a,b)

        
    ''' software
    {
        'DocumentURL': 'https: //sqlite.org/docs.html',
        'FreePlan': True,
        'Features': {
            'ECOM': {
                'ACID': True,
                'DataMode': None,
                'Transactions': True
            },
            'DataBase': {
                'ACID': True,
                'DataMode': None,
                'Transactions': True
            }
        },
        'VendorURL': 'https: //sqlite.org/',
        'Tages': [
            'Ecom',
            'Database',
            'Hello'
        ],
        'FreePlanSpec': 'demo',
        'DemoURL': 'https: //sqlite.org/docs.html',
        'PaidPlanPrice': 0.0,
        'GooglePlusURL': 'https: //plus.google.com/communities/106339046631781940267',
        'FacebookURL': 'https: //www.facebook.com/sqliteviewer/',
        'Screenshots': [
            {
                'Status': None,
                'Vesion': '3.15.0',
                'URL': 'https: //www.facebook.com',
                'Description': 'Firstscreenshots',
                'Title': 'hello'
            }
        ],
        'Logo': 'https: //sqlite.org/',
        'LatestVersion': '3.15.0',
        'Enviroments': {
            'Platform': [
                'Linux',
                'Window',
                'BSD',
                'MacOS'
            ],
            'Language': [
                'Python',
                'Java',
                'PHP',
                'CSharp'
            ],
            'Database': [
                'MySQL',
                'Oracle',
                'MongoDB',
                'MSSQ'
            ]
        },
        'Description': 'Anothergreataspectofthesoftwareis',
        'OpenSorce': True,
        'LicenseTYpe': 'FreeLicense',
        'Status': 'active',
        'Type': 'ECOM',
        'LatestReleaseDate': datetime.date(2016,1,4),
        'PaidPlan': False,
        'VendorName': 'sqlite',
        'URL': 'https: //sqlite.org/',
        'Videos': [
            {
                'Status': None,
                'URL': 'https: //www.facebook.com',
                'Description': 'FirstVideos',
                'Title': 'description'
            }
        ],
        'PaidPlanSpec': 'demo',
        'Summary': 'manyembeddedproducts.',
        'LinkedInURL': 'https: //www.linkedin.com/company/SQLite',
        'DemoVersion': '3.15.0',
        'Name': 'Magento'
    }
    '''       
    ''' products
    {
        'SoftwareType': 'ECOM',
        'SoftwareName': 'Magento',
        'Packages': [
            {
                'System': 'Linux',
                'Name': 'express.mysql',
                'Plan': None,
                'Target': None,
                'Version': None,
                'Database': None,
                'Description': None
            }
        ]
    }
    '''
    
