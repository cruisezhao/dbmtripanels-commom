import json
import requests
import time
import paramiko
import os,sys,re
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth


wordpress = {
    "name": "wordpress2",
    "system": "false","dockerCompose": "wordpress:\n  image: wordpress\n  links:\n    - db:mysql\n  ports:\n    - 8088:80\n\ndb:\n  image: mariadb\n  environment:\n    MYSQL_ROOT_PASSWORD: example\n",
    "rancherCompose": ".catalog:\n  name: \"Wordpress\"\n  version: \"v0.1-educaas1\"\n  description: \"Blog tool, publishing platform and CMS\"\n  uuid: Wordpress-0\n  minimum_rancher_version: v0.51.0\n  questions:    \n    - variable: public_port\n      description: \"public port to access the wordpress site\"\n      label: \"Public Port\"\n      required: true\n      default: \"80\"\n      type: \"int\"\n\n\nwordpress:\n",
    "startOnCreate":"true"
     }

opencart = {

    "name": "opencart",
    "system": "false",
    "dockerCompose": "opencart:\r\n  image: 172.107.32.205:5000/opencart\r\n  ports:\r\n    - 80:80",
    "rancherCompose": ".catalog:\r\n  name: \"Opencart\"\r\n  version: \"v1\"\r\n  description: \"opencart\"\r\n  uuid: Opencart-0\r\n  minimum_rancher_version: v0.51.0\r\n  questions:    \r\n    - variable: public_port\r\n      description: \"public port to access the opencart site\"\r\n      label: \"Public Port\"\r\n      required: true\r\n      default: \"80\"\r\n      type: \"int\"\r\n\r\nopencart:",
    "startOnCreate":"true"

}

Rancher_Url = "http://209.105.243.175"
API_PublicValue = "83F6F46E15BDDB026A2D"
API_SecretValue = "cpNuCJn2i7915WjNYdzUJKsiHFudwKW3CYvfkzgK"
headers = {
    'content-type': 'application/json',
    'Accept': 'application/json'
}

#List environments
def list_env():
    url = Rancher_Url +"/v2-beta/projects"
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    env_result = {}
    environments = []
    for datas in dic["data"]:
        environment = {}
        environment["id"] = datas["id"]
        environment["name"] = datas["name"]
        environment["state"] = datas["state"]
        environments.append(environment)
    env_result["environments"] = environments
    return env_result

#List stacks
def list_stacks(env_id):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/stacks"
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    stack_result = {}
    stacks = []
    for datas in dic["data"]:
        stack = {}
        stack["id"] = datas["id"]
        stack["name"] = datas["name"]
        stack["state"] = datas["state"]
        stacks.append(stack)
    stack_result["stacks"] = stacks
    return stack_result

#List hosts
def list_hosts(env_id):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/hosts"
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    #print (dic)
    host_result = {}
    hosts = []  
    for datas in dic["data"]:
        host = {}
        host["id"] = datas["id"]
        host["hostname"] = datas["hostname"]
        host["state"] = datas["state"]
        host["IP"] = datas["agentIpAddress"]
        labels = {}
        labels = datas["labels"]
        memoryinfo = {}
        memoryinfo = datas["info"]["memoryInfo"]
        host["mem_total"] = memoryinfo["memTotal"]
        host["mem_free"] = memoryinfo["memFree"]
        cpuinfo = {}
        cpuinfo = datas["info"]["cpuInfo"]
        host["CPU count"] = cpuinfo["count"]
        diskinfo = {}
        diskinfo = datas["info"]["diskInfo"]
        host["disk_total"] = diskinfo["mountPoints"]["zpool-docker"]["total"]
        host["disk_free"] = diskinfo["mountPoints"]["zpool-docker"]["free"]
        hosts.append(host)
        host_result["hosts"] = hosts
    return host_result



#List service
def list_services(env_id,stack_id):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/stack/" + stack_id + "/services"
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    service_result = {}
    services = []
    publicEndpoints = []
    for datas in dic["data"]:
        publicEndpoints = datas["publicEndpoints"]
        service = {}
        service["service_id"] = datas["id"]
        service["name"] = datas["name"]
        service["state"] = datas["state"]
        service["stack_id"] = datas["stackId"]
        service["container_id"] = datas["instanceIds"][0]
        services.append(service)
        service_result["services"] = services
        service_result["publicEndpoints"] = publicEndpoints
    return service_result

def list_containers(env_id):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/instances"
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    container_result = {}
    containers = []
    for datas in dic["data"]:
        container = {}
        container["id"] = datas["id"]
        container["name"] = datas["name"]
        container["state"] = datas["state"]
        containers.append(container)
        container_result["containers"] = containers
    return container_result

def container_details(env_id,con_id):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/containers/" + con_id 
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    container_detail_result = {}
    container_details = []
    container_detail = {}
    container_detail["id"] = dic["id"]
    container_detail["name"] = dic["name"]
    container_detail["state"] = dic["state"]
    container_detail["privateIP"] = dic["primaryIpAddress"]
    container_detail["port"] = dic["ports"]
    container_details.append(container_detail)
    container_detail_result["containers"] = container_details
    return container_detail_result


#Create environment
def create_env(name,description):
    data = json.dumps({'name':name,'description':description})
    url = Rancher_Url +"/v2-beta/projects" 
    req = requests.post(url,data,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    create_result = {}
    creates = []
    create = {}
    create["id"] = dic["id"]
    create["name"] = dic["name"]
    creates.append(create)
    create_result["new environment"] = creates
    return create_result

#Create environment api key
def create_api_key(env_id,key_name):
    data = json.dumps({'name':key_name,'description':key_name})
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/apikeys"
    req = requests.post(url,data,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    apikey = {}
    apikeypair = []
    apikey["id"] = dic["id"]
    apikey["name"] = dic["name"]
    apikey["publicValue"] = dic["publicValue"]
    apikey["secretValue"] = dic["secretValue"]
    apikeypair.append(apikey)
    return apikeypair

#Stop stack
def stop_stack(env_id,stack_id):
    data = json.dumps({})
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/stacks/" + stack_id + "/?action=deactivateservices"
    req = requests.post(url,data,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    healthState = dic["healthState"]
    return healthState

#Show stack state
def stack_state(env_id,stack_id):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/stacks/" + stack_id
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    healthState = dic["healthState"]
    return healthState

#Start stack
def start_stack(env_id,stack_id):
    data = json.dumps(wordpress)
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/stacks/" + stack_id + "/?action=activateservices"
    req = requests.post(url,data,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    healthState = dic["healthState"]
    return healthState

#Show service state
def service_state(env_id,service_id):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/services/" + service_id
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()    
    state = dic["state"]
    return state

#Start service
def start_service(env_id,service_id):
    data = json.dumps({})
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/services/" + service_id + "/?action=activate"
    req = requests.post(url,data,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()    
    state = dic["state"]
    return state


#Stop service   
def stop_service(env_id,service_id):
    data = json.dumps({})
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/services/" + service_id + "/?action=deactivate"
    req = requests.post(url,data,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()    
    state = dic["state"]
    return state

# Create stack
def create_stack(env_id,app):     
    data = json.dumps(app)
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/stacks"
    req = requests.post(url,data,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    stack_id = dic["id"]
    return stack_id
       
    

#Delete stack
def delete_stack(env_id,stack_id):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/stacks/" + stack_id
    req = requests.delete(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    time.sleep(2)
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    state = dic["state"]
    return  state


#Add host
def add_host(env_id,host_ip,host_lab,user,host_pwd):
    url = Rancher_Url + "/v2-beta/projects/" + env_id + "/registrationTokens"
    req = requests.post(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    reg_id = dic["id"]
    url_new = url + "/" + reg_id
    req_new = requests.get(url_new,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic_new = req_new.json()
    cmd = dic_new["command"]
    command = cmd.replace('--rm','-e CATTLE_AGENT_IP=\"'+host_ip+'\" -e CATTLE_HOST_LABELS=\''+host_lab+'\' --rm')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host_ip, port=22, username=user, password=host_pwd)
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.readlines()
    for each in result:
        if ("Running Agent" in each ):
            return (each)

#Add IP address on hosting server
def add_ip(primary_ip,user,host_pwd,new_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=primary_ip, port=22, username=user, password=host_pwd)
    stdin, stdout, stderr = ssh.exec_command("ping -c 2 "+new_ip)
    result = str(stdout.read())
    regex=re.compile('100% packet loss')
    if len(regex.findall(result)) == 0:
        return "The ip "+new_ip+" already working somewhere"
    else:
        stdin, stdout, stderr = ssh.exec_command("ifconfig")
        result = stdout.readlines()
        i=0
        while i < len(result):
            if primary_ip in result[i]:
                nic = (result[i-1]).split(' ')
                nic = nic[0]
                break
            i+=1
        nics = []
        for each in result:
            if nic in each:
                 nic1 = (each.split(' '))[0]
                 nics.append(nic1)
        nics.remove(nic)
        nums = []
        for each in nics:
            num = (each.split(':'))[-1]
            nums.append(num)
        nums.sort()
        new_nic = nic+":"+str((int(nums[-1])+1))
        stdin, stdout, stderr = ssh.exec_command("sudo echo >> /etc/network/interfaces && sudo echo auto "+new_nic+" >> /etc/network/interfaces && sudo echo iface "+new_nic+" inet static >> /etc/network/interfaces && sudo echo address "+new_ip+" >> /etc/network/interfaces && sudo echo netmask 255.255.255.0 >> /etc/network/interfaces && sudo service networking restart")
        err = stderr.readlines()
        stdin, stdout, stderr = ssh.exec_command("ping -c 2 "+new_ip)
        result = str(stdout.read())
        regex=re.compile('100% packet loss')
        if len(regex.findall(result)) == 0:
            return "The ip "+new_ip+" is working on this host"
        else:
            return "The ip "+new_ip+" is NOT working on this host"

#Add scheduler ip to rancher
def add_scheduler_ip(env_id,host_id,scheduler_ip):
    url = Rancher_Url +"/v2-beta/projects/" + env_id + "/hosts/" + host_id
    req = requests.get(url,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    ips = dic["labels"]["io.rancher.scheduler.ips"]
    rack = dic["labels"]["Rack"]
    body = {
       "labels": {
       "Rack": rack,
       "io.rancher.scheduler.ips": ips+","+scheduler_ip
    }
    }
    data = json.dumps(body)
    req = requests.put(url,data,auth=HTTPBasicAuth(API_PublicValue, API_SecretValue), headers=headers)
    dic = req.json()
    state = dic["state"]
    return  state
