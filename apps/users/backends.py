'''
Created on Jun 23, 2017

@author: ben
'''
from common.third_party.django.contrib.auth.backends import ModelBackend
from common.apps.users.forms import is_member

class AllowAdminGroupUsersModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return is_member(user, 'admin') or user.is_superuser
        #return True
    
class AllowStaffGroupUsersModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return is_member(user, 'staff') or user.is_superuser