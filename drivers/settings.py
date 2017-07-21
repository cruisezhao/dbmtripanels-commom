import os
Rancher_Url = "http://45.35.12.228:8080" #"http://209.105.243.175"
API_PublicValue = "46473244B678B019FD4C" #"83F6F46E15BDDB026A2D"
API_SecretValue = "NmpPYBT52rckm7kXXfj1chLMHuAbcYBmWZJuR6Pa"#"cpNuCJn2i7915WjNYdzUJKsiHFudwKW3CYvfkzgK"
headers = {
    'content-type': 'application/json',
    'Accept': 'application/json'
}
deploy_info={
    "system": "false",
    "startOnCreate": "true",
}


enviroment_info={
    "Rancher":"1a5",
    "Openstack":"",
    "Rancher1":"1a58"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))