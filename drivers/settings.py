"""

software: software data load and check module.

settings.py: Schema config data.

"""
import sys
import datetime
from schema import Schema, Use, And, Or, Regex, Optional

_DATA_CHECK = True

if sys.version_info[0] == 3:
    basestring = str  # Python 3 does not have basestring
    unicode = str     # Python 3 does not have unicode

map_names = {
    'app_types': {
        'ECOM': 'ECOM',
        'ecom': 'ECOM',
        'cms': 'CMS',
        'db': 'DataBase'
        # '?': basestring
    },
    'vm_types': {
        'linux': 'Linux-VPS',
        'windows': 'Windows-VPS',
        # '?': basestring
    },
    'bare_types': {
        'linux': 'Linux-Bare',
        'windows': 'Windows-Bare',
        # '?': basestring
    },

    'product_types': {
        'APP': 'APP',
        'VM': 'VM',
        'Bare': 'Bare',
        # '?': basestring
    },

    'os_names': {
        'Linux': 'Linux',
        'Window': 'Window',
        'BSD': 'BSD',
        'MacOS': 'MacOS',
        # '?': basestring
    },

    'db_names': {
        'MySQL': 'MySQL',
        'Oracle': 'Oracle',
        'MongoDB': 'MongoDB',
        # '?': basestring
    },

    'languages': {
        'Python': 'Python',
        'Java': 'Java',
        'PHP': 'PHP',
        'CSharp': 'CSharp'
        # '?': basestring
    }  
}

def list_names(dict_names):
    ''' get name list from names dictionary.
    '''
    name_sets = set()
    for nm in dict_names:
        name_sets.add(dict_names[nm])
    return list(name_sets)

d_fmt = '%Y-%m-%d'
_date_validator = Or(None, lambda d: datetime.datetime.strptime(d, d_fmt))

app_types = list_names(map_names['app_types'])
vm_types = list_names(map_names['vm_types'])
bare_types = list_names(map_names['bare_types'])
product_types = list_names(map_names['product_types'])


os_names = list_names(map_names['os_names'])
languages = list_names(map_names['languages'])
db_names = list_names(map_names['db_names'])
 
app_schema = {
    "app_type": Or(*app_types),
    "app_name": basestring,
    "tags": [And(basestring, lambda l: 2< len(l) < 64)],
    "summary": basestring,
    "description": basestring,
    "product_url": basestring,
    "product_pic": basestring,
    "product_img": Or(None, basestring),
    "vendor_name": Or(None, basestring),
    "vendor_url": Or(None, basestring),
    "latest_version": Or(None, basestring),
    "latest_release_date": _date_validator,
    "opensorce": bool,
    "license_type": Or(None, basestring),
    "status": Or(None, int, basestring),
    "demo_url": Or(None, basestring),
    "demo_version": Or(None, basestring),
    "videos": [
        {
            "title": Or(None, basestring),
            "description": Or(None, basestring),
            "url": basestring,
            "status": Or(None, int, basestring)
        }
    ],
    "screenshots": [
        {
            "vesion": Or(None, basestring),
            "title": Or(None, basestring),
            "description": Or(None, basestring),
            "url": basestring,
            "status": Or(None, int, basestring)
        }
    ],
    "facebook_url": Or(None, And(str, lambda s : s.startswith('http'))),
    "google_plus_url": Or(None, And(str, lambda s : s.startswith('http'))),
    "linkedin_url": Or(None, And(str, lambda s : s.startswith('http'))),
    "document_url": Or(None, And(str, lambda s : s.startswith('http'))),
    "free_plan": Or(None, And(str, lambda s : s.startswith('http'))),
    "free_plan_spec": Or(None, basestring),
    "paid_plan": Or(None, basestring),
    "paid_plan_price": Or(int, float),
    "paid_plan_spec": Or(None, basestring),
    "features": {
        str: object,
    },
    "environments": {
        "platform": [Or(*os_names)],
        "language": [Or(*languages)],
        "database": [Or(*db_names)]
    }
}

vm_schema = {
    
}

bare_schema = {
    
}

    
product_schema = {
    'product_type': Or(*product_types),
    'product_name': basestring,
    'plans': [basestring,],
    'deployments':[ {
        'plan_name': basestring,
        'clouds': [basestring]
    },]
}

