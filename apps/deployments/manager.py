'''
Created on Jul 18, 2017

@author: ben
'''

from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class DeployExecutorManager(object):
    MAX_WORKERS = 100
    __executor = None

    @classmethod
    def get_executor(cls):
        if not cls.__executor:
            cls.__executor = ThreadPoolExecutor(max_workers=cls.MAX_WORKERS)
        return cls.__executor

class DeployTaskManager(object):
    __lock = Lock()
    __packages = set()
    
    @classmethod
    def is_deploying(cls, package_id):
        cls.__lock.acquire()
        res = package_id in cls.__packages
        cls.__lock.release()
        return res
    
    @classmethod
    def is_not_deploying_and_set(cls, package_id):
        '''
        returns:
            False: is not deploying
            True: is deploying
        '''
        cls.__lock.acquire()
        is_in = package_id in cls.__packages
        if not is_in:
            cls.__packages.add(package_id)
        cls.__lock.release()
        return is_in
    
    @classmethod
    def deploy_is_over(cls, package_id):
        cls.__lock.acquire()
        cls.__packages.discard(package_id)
        cls.__lock.release()