import yaml
from common.drivers.rancher import apis
from common.drivers import settings


def deploy(deployment_infos):
    '''
    descriptions:
        deploy something to platforms
    parameters:
        deployment_infos:refer to json structure in file: drviers/templates/deploy.json
    returns:
        deploy_id
        deploy_id means stack id for Rancher;
    '''
    
    fr1=open("../drivers/templates/rancher_images_cloudid.yml",'r')
    urls=yaml.load(fr1)[deployment_infos["product_name"]]
    URL=""
    for url in urls:
        if url["database"]==deployment_infos["servers"][0]["server_configurations"]["DataBase"] and url["operating_system"]==deployment_infos["servers"][0]["server_configurations"]["OS"]:
            URL=url["template_url"]
            break
    fr2=open(URL,'r')
    tri_compose=yaml.load(fr2)
    cloud_name=deployment_infos["servers"][0]["cloud_name"]
    if 'rancher' in cloud_name.lower():
        app_dict={}
        #     "name": "",
        #     "system": "",
        #     "dockerCompose": "",
        #     #"rancherCompose": "",
        #     "startOnCreate": ""
        app_dict["name"] = tri_compose["name"]
        app_dict["system"] = settings.deploy_info["system"]
        app_dict["startOnCreate"]=settings.deploy_info["startOnCreate"]
        tri_docker=tri_compose["docker"]
        for server in tri_docker:
            tri_docker[server]["mem_limit"]=(deployment_infos["servers"][0]["memory"])*1024*1024
            tri_docker[server]["cpu_quota"]=(deployment_infos["servers"][0]["cpu"])*24*2*100000/100
        #tri_rancher=x["rancher"]
        final_docker=yaml.dump(tri_docker)
        #final_rancher = yaml.dump(tri_rancher)
        #app_dict["rancherCompose"]=final_rancher#wordpress["rancherCompose"]
        app_dict["dockerCompose"]=final_docker
        result=apis.create_stack(settings.enviroment_info[cloud_name],app_dict)
    return result
def get_deployment_state(cloud_name, deploy_id):
    '''
    descriptions:
        query deployment states
    parameters:
        cloud_name:  platform id
        deploy_id: comes from deloy API function,
                   deploy_id means stack id for Rancher,
                   callee distinguishes platforms by cloud_name
    returns:
        {retcode, descriptions}
        retcode: 0~success, 1~deploy is in progress, 2~failure
        descriptions: describe reasons for failure
    '''
    result={}
    if 'rancher' in cloud_name.lower():
        res=apis.stack_state(settings.enviroment_info[cloud_name],deploy_id)
        # stack_state: active, activing, error
        if res["state"]=="active":
            result["retcode"]=0
        else:
            if res["state"]=="activating":
                result["retcode"]=1
            else:
                result["retcode"]=2
                result["descriptions"]=res["message"]
    return result

def get_deployment_details(cloud_name, deploy_id):
    '''
    descriptions:
        query details after deployment successed
    parameters:
        cloud_name:  platform id
        deploy_id: comes from deploy API function,
                   deploy_id means stack id for Rancher
                   callee distinguishes platforms by cloud_name
    returns:
        {cloud_name, details:[{stack_id, service_id, containers:[container_id,name,port,privateIP,state,host_id]}]}

        container_ids: is array structure

        WARNING:structure above is only for Rancher,
                for OpenStack, return structure maybe different,
                caller distinguishes it by cloud_name
    '''
    result={}
    if 'rancher' in cloud_name.lower():
        result["cloud_name"] = cloud_name
        stack_list=[]
        stack_detail={}
        search_res = apis.list_services(settings.enviroment_info[cloud_name],deploy_id)
        for service in search_res["services"]:
            stack_detail["stack_id"]=deploy_id
            stack_detail["service_id"]=service["service_id"]
            containers=service["container_ids"]
            container_list=[]
            for container in containers:
                container_detail=apis.container_details(settings.enviroment_info[cloud_name],container)
                container_list.append(container_detail)
                stack_detail["containers"] = container_list
            stack_list.append(stack_detail)
        result["details"]=stack_list
    return result

def get_login_details(cloud_name, deploy_id):
    '''
    descriptions:
        query login informations for clients
    parameters:
        cloud_name:  platform id
        deploy_id: comes from deploy API function,
                   deploy_id means stack id for Rancher,
                   callee distinguishes platforms by cloud_name
    returns:
        {cloud_name, logins:[{destination_id, URL, user_name, password}]}

        destination_id: is an abstract concept.
                        it is service_id for Rancher, server_id for OpenStack

        WARNING:some return parameters may be empty for certain platform,
                for example, user_name, password are empty for Rancher,
                caller distinguishes it by cloud_name
    '''
    result={}
    if 'rancher' in cloud_name.lower():
        result["cloud_name"]=cloud_name
        login_list=[]
        login_details = {}
        search_res = apis.list_services(settings.enviroment_info[cloud_name],deploy_id)
        for service in search_res["publicEndpoints"]:
            login_details["destination_id"]=service["serviceId"]
            login_details["URL"]=service["ipAddress"]
            login_list.append(login_details)
        result["logins"]=login_list
    return  result
def delete_deploy(cloud_name, deploy_id):
    '''
    descriptions:
        delete product deployed
    parameters:
        cloud_name:  platform id
        deploy_id: comes from deploy API function,
                   deploy_id means stack id for Rancher,
                   callee distinguishes platforms by cloud_name
    returns:
        state:  current state, values can be:
    '''
    if 'rancher' in cloud_name.lower():
        current_state=apis.delete_stack(settings.enviroment_info[cloud_name],deploy_id)
    return  current_state


def start(cloud_name, server_id):
    '''
    descriptions:
        start server/service stopped
    parameters:
        cloud_name:  platform id
        server_id: means service_id for Rancher;
                   means server_id for Openstack
                   callee distinguishes platforms by cloud_name
    returns:
        state: current state, values can be:
    '''
    if 'rancher' in cloud_name.lower():
        current_state=apis.start_service(settings.enviroment_info[cloud_name],server_id)
    return  current_state

def stop(cloud_name, server_id):
    '''
    descriptions:
        stop server/service started
    parameters:
        cloud_name:  platform id
        server_id: means service_id for Rancher;
                   means server_id for Openstack
                   callee distinguishes platforms by cloud_name
    returns:
        state: current state, values can be:
    '''
    if 'rancher' in cloud_name.lower():
        current_state=apis.stop_service(settings.enviroment_info[cloud_name],server_id)
    return  current_state


def get_server_state(cloud_name, server_id):
    '''
    descriptions:
        get server/service state
    parameters:
        cloud_name:  platform id
        server_id: means service_id for Rancher;
                   means server_id for Openstack
                   callee distinguishes platforms by cloud_name
    returns:
        state: current state, values can be:'Active','Deactive'
    '''
    if 'rancher' in cloud_name.lower():
            current_state=apis.service_state(settings.enviroment_info[cloud_name],server_id)
    return current_state
if __name__=='__main__':
    recived_dict={
        #"template_url":"C:/Users/admin/Documents/TriPanel/common/drivers/templates/tripanels-compose.yml",
        "product_name":"OsCommerce",
        "servers": [{
            "cloud_name": "Rancher",
            "cpu": 2,
            "memory": 20,
            "disk": 200,
        "server_configurations": {
            "OS":"Ubuntu 16.04",
            "DataBase":"MySQL 5.7",
        }}],
        "answers": {
            "cloud": "tripanels",
            "proxy_scheme": "https"
        }
    }
    #test deploy()
    stack_id=deploy(recived_dict)
    print(stack_id)
    # res0=get_deployment_state(recived_dict["servers"][0]["cloud_name"],"1st162")
    # print("deployment_state")
    # print(res0)
    # res1=get_deployment_details(recived_dict["servers"][0]["cloud_name"],"1st162")
    # print("deployment_details")
    # print(res1)
    # print(yaml.dump(res1))
    # res2=get_login_details(recived_dict["servers"][0]["cloud_name"],"1st162")
    # print("login_details")
    # print(res2)
    # res5=stop(recived_dict["servers"][0]["cloud_name"],"1s167")
    # print(res5)
    # res4=get_server_state(recived_dict["servers"][0]["cloud_name"],"1s167")
    # print(res4)
    # res6=start(recived_dict["servers"][0]["cloud_name"],"1s167")
    # print(res6)
    # res3=delete_deploy(recived_dict["servers"][0]["cloud_name"],"1st162")
    # print(res3)

