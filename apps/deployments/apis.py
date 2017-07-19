'''
Created on Jul 17, 2017

@author: ben
'''
from common.apps.deployments.models import Servers,\
    ServerContainers, ServerVMs
from django.db import transaction
from common.drivers import gateway

from common.apps.packages.models import Packages
from .manager import DeployExecutorManager
from common.apps.deployments.manager import DeployTaskManager


DEPLOY_SUCCESS = 0
DEPLOY_FAILURE = 1
DEPLOY_TIME_OUT = 2   



    
def _get_server_type_by_cloud(cloud):
    if 'rancher' in cloud.name.lower():
        return 'Container'
    elif 'openstack' in cloud.name.lower():
        return 'VirtualMachine'
    else:
        return 'BareMetal'

def _get_driver_deploy_parameter(deploy_infos):
    ret_infos = {}
    ret_infos['product_name'] = deploy_infos['product_name']
    ret_infos['servers'] = []
    for dict_server in deploy_infos['servers']:
        server = {}
        server['cloud'] = dict_server['cloud'].id
        server['cpu'] = dict_server['cpu']
        server['memory'] = dict_server['memory']
        server['disk'] = dict_server['disk']
        
        server['server_configurations'] = {}
        for option in dict_server['server_configurations']:
            server['server_configurations'][option.type] = option.value
        ret_infos['servers'].append(server)   
         
    ret_infos['answers'] = deploy_infos['answers']    
    return ret_infos

def _test():
    deploy_infos = {}
    package_id = 1
    
    timeout_s = 60*10
    interval_s = 10
    deploy_id = deploy(deploy_infos, make_callback(package_id), timeout_s, interval_s)
    
    
def make_callback(package_id):
    def callback(future):
        try:
            res = future.result()
            package = Packages.objects.get(id = package_id)
            if res['retcode'] == DEPLOY_SUCCESS:
                package.deploy_status = 'Success'
                package.status = 'Active'
            elif res['retcode'] == DEPLOY_FAILURE:
                package.deploy_status = 'Failure'
            elif res['retcode'] == DEPLOY_TIME_OUT:
                package.deploy_status = 'Timeout'
            else:
                print('error deploy result type')
            
            if res['retcode'] == DEPLOY_SUCCESS:
                servers = Servers.objects.filter(deploy_id = res['deploy_id'])
                
                for server in servers:
                    server.package = package
                    
                with transaction.atomic():      
                    package.save()
                    for s in servers:
                        s.save()
        finally:
            DeployTaskManager.deploy_is_over(package_id)
    return callback    


def deploy(deploy_infos, callback, timeout_s, interval_s):
    
    '''
    callback: a callback function, will be called after deploy completed, with the future as its only argument
    
    input parameter:
{
    "client":client,
    "product_name":"Magento",
    "servers":[ {
        "cloud":cloud,
        "cpu": 2,
        "memory": 20,
        "disk": 200,
        "server_configurations":[system_option1,system_option2]
    }],
    "answers": {
        "cloud": "tripanels",
        "proxy_scheme": "https"
    }
}
    return:
        deploy_id
        
        
Driver Gateway deploy API input parameter:
{
    "product_name":'Magento',
    "servers":[ {
        "cloud":cloud_id,
        "cpu": 2,
        "memory": 20,
        "disk": 200,
        "server_configurations":{'OS':'Ubuntu16.04','DataBase':'Mysql5.7',}
    }],
    "answers": {
        "cloud": "tripanels",
        "proxy_scheme": "https"
    }
}
    return:
        deploy_id
    '''
    with transaction.atomic(): 
        servers = []
        for dict_server in deploy_infos['servers']:
            #client = deploy_infos['client']
            srv_type = _get_server_type_by_cloud(dict_server['cloud'])
            if Servers.is_type_container(srv_type): 
                srv = ServerContainers(total_cores=dict_server['cpu'], 
                          total_memory=dict_server['memory'], type=srv_type)
            elif Servers.is_type_VM(srv_type):
                srv = ServerVMs(total_cores=dict_server['cpu'], 
                          total_memory=dict_server['memory'], type=srv_type)
            else:
                raise Exception('error server type')
            
            srv.save()
            for option in dict_server['server_configurations']:
                    #config = ServerConfigurations(server=srv,system_option=option)
                    srv.system_options.add(option)    
                    
            servers.append(srv)
    
        
        driver_deploy_infos = _get_driver_deploy_parameter(deploy_infos)
        
        #in a app installation, 
        #there maybe different platforms(cloud ids), and different deploy processes,
        #so we need group servers by cloud id, and then call gateway deploy function several times
        #passing different parameters groupped by servers by cloud id.
        deploy_id = _driver_deploy(driver_deploy_infos) 
        
        for server in servers:
            server.deploy_id = deploy_id
            server.save()

    #start a thread to query deploy state
    exe = DeployExecutorManager.get_executor()
    future = exe.submit(_get_deploy_state, driver_deploy_infos['servers'][0]['cloud'], deploy_id, timeout_s, interval_s)
    future.add_done_callback(callback) 

    
    return deploy_id

def retry_deploy(deploy_id, product_name):
    servers = Servers.objects.filter(deploy_id = deploy_id)

def _flaten_services_to_containers(service_dict):
    '''
    details:[{stack_id, service_id, containers:[id,name,port,privateIP,state,host_id]}]
    =>
    details:[{stack_id, service_id, container_id,container_name,port,privateIP,state,host_id}]
    '''
    res = []
    for service in service_dict:
        for c in service['containers']:
            container = {}
            container['stack_id'] = service['stack_id']
            container['service_id'] = service['service_id']
            container['container_id'] = c['id']
            container['container_name'] = c['name']
            container['port'] = c['port']
            container['privateIP'] = c['privateIP']
            container['state'] = c['state']
            container['host_id'] = c['host_id']
            res.append(container)
    return res

# stack_id = '123456'
# service_id = '789'    
# container_id = '00012345'
# host_id = '9999'
def _get_deployment_details(cloud_id, deploy_id):
    '''
    {cloud_id, details:[{stack_id, service_id, containers:[id,name,port,privateIP,state,host_id]}]}
    '''
#     global stack_id, service_id,container_id,host_id
#     import random
#     service_id = str(random.uniform(100, 999))
#     container_id = str(random.uniform(1000, 9999))
#     return {'cloud_id' : 1, 'details':[{'stack_id':stack_id, 'service_id':service_id, \
#                                         'containers':[{'id':container_id, 'name':'ben','port':['209.105.243.70:80:80/tcp'],'privateIP':'','state':'running','host_id':host_id},]}]}
    return gateway.get_deployment_details(cloud_id, deploy_id) 

def _get_deployment_state(cloud_id, deploy_id):
#     return {'retcode':0, 'descriptions':'success'}
    return gateway.get_deployment_state(cloud_id, deploy_id)           

def _driver_deploy(driver_deploy_infos):
#     import random
#     global stack_id
#     stack_id = str(random.uniform(10, 99))
#     return stack_id
    return gateway.deploy(driver_deploy_infos)

def _get_deploy_state(cloud_id, deploy_id, timeout_s, interval_s):
    '''
    return {'retcode':DEPLOY_SUCCESS, 'deploy_id':deploy_id}
    '''
    import time
    import traceback
    times = timeout_s // interval_s + 1
    try:
        for _ in range(times):
            state = _get_deployment_state(cloud_id, deploy_id)
            if state['retcode'] == 0:
                #success
                res = _get_deployment_details(cloud_id, deploy_id)
                servers = Servers.objects.filter(deploy_id = deploy_id)
                real_servers = []
                for (server,detail) in zip(servers, _flaten_services_to_containers(res['details'])):
                    if server.is_container():
                        container = server.servercontainers
                        container.peer_id = detail['container_id']
                        host_server = Servers.objects.get(peer_id=detail['host_id'])
                        container.device = host_server.device
                        container.stack_id = detail['stack_id']
                        container.service_id = detail['service_id']
                        container.container_id = detail['container_id']
                        real_servers.append(container)
                        #to do: IP address 
                with transaction.atomic():        
                    for real_server in real_servers:
                        real_server.save()
                        
                return {'retcode':DEPLOY_SUCCESS, 'deploy_id':deploy_id}
            
            elif state['retcode'] == 1:
                #in progress
                time.sleep(interval_s)
                continue
            else:
                #failed
                return {'retcode':DEPLOY_FAILURE, 'deploy_id':deploy_id}
    except Exception as e:
        print('get_deploy_state occurs exceptions: ')
        print(e)
        traceback.print_stack()
        return {'retcode':DEPLOY_FAILURE, 'deploy_id':deploy_id}
        
    
    return {'retcode':DEPLOY_TIME_OUT, 'deploy_id':deploy_id}


    