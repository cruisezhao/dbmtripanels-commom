import yaml
from common.drivers.rancher import apis

app_dict={
    "name": "",
    "system": "",
    "dockerCompose": "",
    #"rancherCompose": "",
    "startOnCreate": ""
    }
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
    urls=yaml.load(fr1)[deployment_infos["name"]]
    URL=""
    for url in urls:
        if url["database"]==deployment_infos["server_configurations"]["database"] and url["operating_system"]==deployment_infos["server_configurations"]["operating_system"]:
            URL=url["template_url"]
    fr2=open(URL,'r')
    tri_compose=yaml.load(fr2)
    if deployment_infos["cloud_type"] == "Rancher":
        app_dict["name"]=tri_compose["name"]
        app_dict["system"]=deployment_infos["system"]
        app_dict["startOnCreate"]=deployment_infos["startOnCreate"]
        tri_docker=tri_compose["docker"]
        #tri_rancher=x["rancher"]
        final_docker=yaml.dump(tri_docker)
        #final_rancher = yaml.dump(tri_rancher)
        #app_dict["rancherCompose"]=final_rancher#wordpress["rancherCompose"]
        app_dict["dockerCompose"]=final_docker
        result=apis.create_stack(deployment_infos["service"]["cloud_id"],app_dict)
    return result
def get_deployment_state(cloud_id, deploy_id):
    '''
    descriptions:
        query deployment states
    parameters:
        cloud_id:  platform id
        deploy_id: comes from deloy API function,
                   deploy_id means stack id for Rancher,
                   callee distinguishes platforms by cloud_id
    returns:
        {retcode, descriptions}
        retcode: 0~success, 1~deploy is in progress, 2~failure
        descriptions: describe reasons for failure
    '''
    res=apis.stack_state(cloud_id,deploy_id)
    # stack_state: active, activing, error
    result={}
    if res["state"]=="active":
        result["retcode"]=0
    else:
        if res["state"]=="activating":
            result["retcode"]=1
        else:
            result["retcode"]=2
            result["descriptions"]=res["message"]
    return result

def get_deployment_details(cloud_id, deploy_id):
    '''
    descriptions:
        query details after deployment successed
    parameters:
        cloud_id:  platform id
        deploy_id: comes from deploy API function,
                   deploy_id means stack id for Rancher
                   callee distinguishes platforms by cloud_id
    returns:
        {cloud_id, details:[{stackid, service_id, container_ids}]}

        container_ids: is array structure

        WARNING:structure above is only for Rancher,
                for OpenStack, return structure maybe different,
                caller distinguishes it by cloud_id
    '''
    result={}
    racher_env=apis.list_env()
    for env in racher_env["environments"]:
        if cloud_id == env["id"]:
            result["cloud_id"] = cloud_id
            stack_list=[]
            stack_detail={}
            search_res = apis.list_services(cloud_id,deploy_id)
            for service in search_res["services"]:
                stack_detail["stack_id"]=deploy_id
                stack_detail["service_id"]=service["service_id"]
                stack_detail["container_ids"] = service["container_id"]
                stack_list.append(stack_detail)
            result["details"]=stack_list
    return result

def get_login_details(cloud_id, deploy_id):
    '''
    descriptions:
        query login informations for clients
    parameters:
        cloud_id:  platform id
        deploy_id: comes from deploy API function,
                   deploy_id means stack id for Rancher,
                   callee distinguishes platforms by cloud_id
    returns:
        {cloud_id, logins:[{destination_id, URL, user_name, password}]}

        destination_id: is an abstract concept.
                        it is service_id for Rancher, server_id for OpenStack

        WARNING:some return parameters may be empty for certain platform,
                for example, user_name, password are empty for Rancher,
                caller distinguishes it by cloud_id
    '''
    result={}
    racher_env=apis.list_env()
    for env in racher_env["environments"]:
        if cloud_id == env["id"]:
            result["cloud_id"]=cloud_id
            login_list=[]
            login_details = {}
            search_res = apis.list_services(cloud_id,deploy_id)
            for service in search_res["publicEndpoints"]:
                login_details["destination_id"]=service["serviceId"]
                login_details["URL"]=service["ipAddress"]
                login_list.append(login_details)
            result["login"]=login_list
    return  result
def delete_deploy(cloud_id, deploy_id):
    '''
    descriptions:
        delete product deployed
    parameters:
        cloud_id:  platform id
        deploy_id: comes from deploy API function,
                   deploy_id means stack id for Rancher,
                   callee distinguishes platforms by cloud_id
    returns:
        state:  current state, values can be:
    '''
    result={}
    racher_env=apis.list_env()
    for env in racher_env["environments"]:
        if cloud_id == env["id"]:
            current_state=apis.delete_stack(cloud_id,deploy_id)
            break
    return  current_state


def start(cloud_id, server_id):
    '''
    descriptions:
        start server/service stopped
    parameters:
        cloud_id:  platform id
        server_id: means service_id for Rancher;
                   means server_id for Openstack
                   callee distinguishes platforms by cloud_id
    returns:
        state: current state, values can be:
    '''
    racher_env=apis.list_env()
    for env in racher_env["environments"]:
        if cloud_id == env["id"]:
            current_state=apis.start_service(cloud_id,server_id)
            break
    return  current_state

def stop(cloud_id, server_id):
    '''
    descriptions:
        stop server/service started
    parameters:
        cloud_id:  platform id
        server_id: means service_id for Rancher;
                   means server_id for Openstack
                   callee distinguishes platforms by cloud_id
    returns:
        state: current state, values can be:
    '''
    racher_env=apis.list_env()
    for env in racher_env["environments"]:
        if cloud_id == env["id"]:
            current_state=apis.stop_service(cloud_id,server_id)
            break
    return  current_state


def get_server_state(cloud_id, server_id):
    '''
    descriptions:
        get server/service state
    parameters:
        cloud_id:  platform id
        server_id: means service_id for Rancher;
                   means server_id for Openstack
                   callee distinguishes platforms by cloud_id
    returns:
        state: current state, values can be:'Active','Deactive'
    '''
    racher_env=apis.list_env()
    for env in racher_env["environments"]:
        if cloud_id == env["id"]:
            current_state=apis.service_state(cloud_id,server_id)
            break
    return current_state
if __name__=='__main__':
    recived_dict={
        #"template_url":"C:/Users/admin/Documents/TriPanel/common/drivers/templates/tripanels-compose.yml",
        "name":"Magento",
        "cloud_type":"Rancher",
        "cloud_location":"USA_TX_Dallas",
        "cloud_user":"",
        "cloud_user_password":"",
        "deploy_id":"1st130",
        "service_id":"1st136",
        "system": "false",
        "startOnCreate": "true",
        "service": {
            "cloud_id":"1a5",
            "cpu": 2,
            "memory": 20,
            "disk": 200,
        },
        "server_configurations": {
            "operating_system":"Ubuntu 16.04",
            "database":"MySQL 5.7",
        },
        "answers": {
            "cloud": "tripanels",
            "proxy_scheme": "https"
        }
    }
    #test deploy()
    # stack_id=deploy(recived_dict)
    # print(stack_id)
    # res0=get_deployment_state(recived_dict["service"]["cloud_id"],recived_dict["deploy_id"])
    # print("deployment_state")
    # print(res0)
    # res1=get_deployment_details(recived_dict["service"]["cloud_id"],recived_dict["deploy_id"])
    # print("deployment_details")
    # print(res1)
    # res2=get_login_details(recived_dict["service"]["cloud_id"],recived_dict["deploy_id"])
    # print("login_details")
    # print(res2)
    # res3=delete_deploy(recived_dict["service"]["cloud_id"],recived_dict["deploy_id"])
    # print(res3)
    res4=get_server_state(recived_dict["service"]["cloud_id"],recived_dict["service_id"])
    print(res4)
