"""

Openstack: Service module for openstack platform integration.

server.py: Common function for server management .

"""
import json
import requests
api_host = '45.35.12.10'
auth_api_root = '45.35.12.10:5000/v3'

def auth_tokens(name, password, domain_name='Default'):
    """Authorized by user name and password."""
    data = {
        'auth': {
            'identity': {
                'methods': ['password'],
                'password': {
                    'user': {
                        'name': name,
                        'domain': {'name': domain_name},
                        'password': password
                    }
                }
            }
        }
    }
    
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json'
    }
    
    url = 'http://%s/auth/tokens' % auth_api_root
    
    req = requests.post(url, data=json.dumps(data), headers=headers)
    result = {}
    jsond = req.json()
    if req.status_code == 201 and jsond['token'].get('project', None) is not None:
        result['code'] = 200
        tokens = {}
        tokens['id'] = req.headers.get('X-Subject-Token', '')
        tokens['project'] = jsond['token']['project']
        tokens['user'] = jsond['token']['user']
        api_url = {'nova': {}}
        for catalog in jsond['token']['catalog']:
            if catalog['name'] == 'nova':
                for endpoint in catalog['endpoints']:
                    api_url['nova'][endpoint['interface']] = endpoint['url']

        tokens['api_url'] = api_url
        result['tokens'] = tokens
    else:
        result['code'] = req.status_code
        result['msg'] = 'Incorrect user name or password.'
    return result


def servers_detail(token_id, api_url):
    """Get all servers with detail information by project id"""
    
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': token_id
    }
    
    url = api_url + '/servers/detail'
    
    req = requests.get(url, headers=headers)
    result = {}
    result['code'] = req.status_code
    if result['code'] == 200:
        jsond = req.json()
        servers = []
        for server in jsond['servers']:
            svr = {}
            svr['name'] = server['name']
            svr['updated'] = server['updated']
            svr['addr'] = server['addresses']['provider'][0]['addr']
            svr['id'] = server['id']
            svr['status'] = server['status']
            svr['created'] = server['created']
            servers.append(svr)

        result['servers'] = servers
    else:
        result['msg'] = req.json()['error']['message']
    return result


def server_detail(token_id, api_url, server_id):
    """Get single server detail information by server id."""
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': token_id
    }
    
    url = api_url + '/servers/' + server_id
    
    req = requests.get(url, headers=headers)
    result = {}
    result['code'] = req.status_code
    if result['code'] == 200:
        jsond = req.json()['server']
        server = {}
        server['created'] = jsond['created']
        server['task_state'] = jsond['OS-EXT-STS:task_state']
        server['name'] = jsond['name']
        server['id'] = jsond['id']
        server['user_id'] = jsond['user_id']
        server['volumes_attached'] = jsond['os-extended-volumes:volumes_attached']
        server['mac_addr'] = jsond['addresses']['provider'][0]['OS-EXT-IPS-MAC:mac_addr']
        server['type_addr'] = jsond['addresses']['provider'][0]['OS-EXT-IPS:type']
        server['version_addr'] = jsond['addresses']['provider'][0]['version']
        server['addr'] = jsond['addresses']['provider'][0]['addr']
        server['accessIPv4'] = jsond['accessIPv4']
        server['accessIPv6'] = jsond['accessIPv6']
        server['image_id'] = jsond['image']['id']
        server['terminated_at'] = jsond['OS-SRV-USG:terminated_at']
        server['launched_at'] = jsond['OS-SRV-USG:launched_at']
        server['power_state'] = jsond['OS-EXT-STS:power_state']
        server['status'] = jsond['status']
        server['updated'] = jsond['updated']
        server['vm_state'] = jsond['OS-EXT-STS:vm_state']
        server['flavor_id'] = jsond['flavor']['id']
        server['hostId'] = jsond['hostId']
        server['tenant_id'] = jsond['tenant_id']
        server['diskConfig'] = jsond['OS-DCF:diskConfig']
        server['config_drive'] = jsond['config_drive']
        server['key_name'] = jsond['key_name']
        server['availability_zone'] = jsond['OS-EXT-AZ:availability_zone']
        server['progress'] = jsond['OS-EXT-AZ:availability_zone']
        result['server'] = server
    else:
        result['msg'] = req.json()['error']['message']
    return result


def project_quota(token_id, api_url):
    """Get project usage data by project id."""
    url_t = api_url.split('/')
    new_url = api_url.rstrip(url_t[-1]) + 'os-quota-sets/' + url_t[-1]
    
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': token_id
    }
    
    req = requests.get(new_url, headers=headers)
    result = {}
    result['code'] = req.status_code
    if result['code'] == 200:
        result['quota'] = req.json()['quota_set']
    else:
        result['msg'] = req.json()['error']['message']
    return result


def server_action(token_id, api_url, server_id, action):
    """Server action api, include start, stop, reboot, shutdown etc."""
    action_data = {
        'start': {'os-start': None},
        'stop': {'os-stop': None},
        'soft_reboot': {
            'reboot': {'type': 'SOFT'}
        },
        'hard_reboot': {
            'reboot': {'type': 'HARD'}
        }
    }
    
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': token_id
    }
    
    url = api_url + '/servers/' + server_id + '/action'
    req = requests.post(url, data=json.dumps(action_data[action]), headers=headers)
    result = {}
    result['code'] = req.status_code
    if result['code'] == 202:
        result['code'] = 200
    else:
        result['msg'] = req.json()
    return result


def server_console(token_id, api_url, server_id):
    """Get noVNC url"""
    data = {
        'os-getVNCConsole': {'type': 'novnc'}
    }
    
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': token_id
    }
    
    url = api_url + '/servers/' + server_id + '/action'
    req = requests.post(url, data=json.dumps(data), headers=headers)
    result = {}
    result['code'] = req.status_code
    if result['code'] == 200:
        result['console'] = req.json()['console']
    else:
        result['msg'] = req.json()['error']['message']
    return result


def project_limits(token_id, api_url):
    """Get project limites by project id"""
    
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': token_id
    }
    url = api_url + '/limits'
    
    req = requests.get(url, headers=headers)
    result = {}
    result['code'] = req.status_code
    if result['code'] == 200:
        result['limits'] = req.json()['limits']['absolute']
        result['limits']['totalRAMUsed'] = \
        int(result['limits']['totalRAMUsed'] / 1024)
        result['limits']['maxTotalRAMSize'] = \
        int(result['limits']['maxTotalRAMSize'] / 1024)
    else:
        result['msg'] = req.json()['error']['message']
    return result


def servers_quota(token_id, api_url):
    """Get all servers  with quota information by project id."""
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': token_id
    }
    
    url = api_url + '/servers/detail'
    
    req = requests.get(url, headers=headers)
    result = {}
    result['code'] = req.status_code
    if result['code'] == 200:
        jsond = req.json()
        servers = []
        for server in jsond['servers']:
            url = api_url + '/flavors/' + server['flavor']['id']
            fr = requests.get(url, headers=headers)
            if fr.status_code == 200:
                inst = {}
                flavor = fr.json()['flavor']
                inst['id'] = server['id']
                inst['task_state'] = server['status']
                inst['name'] = server['name']
                inst['addr'] = server['addresses']['provider'][0]['addr']
                inst['ram'] = int(flavor['ram'] / 1024)
                inst['disk'] = flavor['disk']
                inst['vcpus'] = flavor['vcpus']
                inst['created'] = server['created']
                servers.append(inst)

        result['servers'] = servers
    else:
        result['msg'] = req.json()['error']['message']
    return result


def project_overview(token_id, api_url):
    """Get project profile by project id."""
    limits = project_limits(token_id, api_url)
    quotas = servers_quota(token_id, api_url)
    result = {}
    if limits['code'] == 200 and quotas['code'] == 200:
        result['code'] = 200
        result['limits'] = limits['limits']
        result['servers'] = quotas['servers']
    else:
        result['code'] = 500
        result['msg'] = 'Server internal error.'
    return result


if __name__ == '__main__':
    pass

