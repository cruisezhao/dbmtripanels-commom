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

d_fmt = '%Y-%m-%d'
_date_validator = Or(None, lambda d: datetime.datetime.strptime(d, d_fmt))

software_types = ["ECOM","CMS","DataBase"]
platforms = ["Linux","Window","BSD","MacOS"]
languages = ["Python","Java","PHP","CSharp","Go"]
db_names = ["MySQL","Oracle","MongoDB",str] 
 
software_schema = {
    "type": Or(*software_types),
    "name": basestring,
    "tags": [And(basestring, lambda l: 2< len(l) < 64)],
    "summary": basestring,
    "description": basestring,
    "software_url": basestring,
    "software_pic": basestring,
    "software_img": Or(None, basestring),
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
        "platform": [Or(*platforms)],
        "language": [Or(*languages)],
        "database": [Or(*db_names)]
    }
}

products_schema = {
    "software_type": Or(*software_types),
    "software_name": basestring,
    "packages": [
        {
            "name": Or(None, basestring),
            "version": basestring,
            "description": Or(None, basestring),
            "system": Or(None, object),
            "database": Or(None, object),
            "target": Or(None, basestring),
            "plans": [
                basestring,
            ]
        }
    ],                  
    "plans": {
        basestring: {
            "cpu_cores": int,
            "memory": int,
            "disks": {'sata': int, 'ssd': int},
            "bandwidth": int,
            "servers": [
                {
                    "name": basestring,
                    "description": Or(None, basestring),
                    "cpu_cores": int,
                    "memory": int,
                    "disks": [{'sata': int, 'ssd': int},],
                    "ip_address": Or(None, basestring),
                    "user_name": Or(None, basestring),
                    "password": Or(None, basestring),
                    "applications": [
                        {
                            "name": Or(None, basestring),
                            "description": Or(None, basestring),
                            "url": Or(None, basestring),
                            "user_name": Or(None, basestring),
                            "password": Or(None, basestring)
                        }
                    ]
                }
            ],
            "fees": {
                "price": Or(int, float),
                "discount": Or(int, float)
            }
        },        
    }
}