'''
Created on Jun 13, 2017

@author: ben
'''

from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()

class AuthenticationFormWithAdminGroupOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not is_member(user, 'admin'):
            raise ValidationError(
                _("This account dose not belong to admin group."),
                code='admingroup',
            )
 
class AuthenticationFormWithStaffGroupOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not is_member(user, 'staff'):
            raise ValidationError(
                _("This account dose not belong to staff group."),
                code='staffgroup',
            )   