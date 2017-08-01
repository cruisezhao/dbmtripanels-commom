'''
Created on Jun 23, 2017

@author: ben
'''
from django.contrib.auth.backends import ModelBackend
from common.apps.users.forms import is_member

class AllowAdminGroupUsersModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        is_superuser = getattr(user, 'is_superuser', None)
        print('is_superuser', is_superuser)
        print('is admin member', is_member(user, 'admin'))
        return is_member(user, 'admin') or is_superuser or is_superuser is None
    
class AllowStaffGroupUsersModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        is_superuser = getattr(user, 'is_superuser', None)
        # print('is_superuser', is_superuser)
        # print('is staff member', is_member(user, 'staff'))
        return is_member(user, 'staff') or is_superuser or is_superuser is None