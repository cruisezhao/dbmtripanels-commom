from django.core import signing
from django.core.urlresolvers import reverse
import hmac
import time
import os
from django.conf import settings

def path_and_rename(instance, filename):
           
    newfilename = hmac.new(settings.SECRET_KEY.encode(), (instance.email + time.strftime('%Y_%m_%d_%H_%M_%S')).encode()).hexdigest() \
        + os.path.splitext(filename)[1]
    userid_hmac = hmac.new(settings.SECRET_KEY.encode(), (str(instance.pk)).encode()).hexdigest()        
    return os.path.join('photo', 'user_'+userid_hmac, newfilename)


def get_signer(salt='register_email_confirm'):
    """ get the timestamp sign
    :param salt:
    :return timestampsign object
    """
    return signing.TimestampSigner(salt=salt)


def get_confirmation_url(email,request,username=None):
    """
        Return confirmation url
        :param email
        :return: string of url
    """
    singer = get_signer()
    code_list = [email,'']
    if username:
        code_list[1] = username
    code = singer.sign(':'.join(code_list))
    url = request.build_absolute_uri(reverse('accounts:email_confirmation',kwargs={'code':code}))
    return url


def create_code(email):
    """create code ,use this code verify the user"""
    singer = get_signer()
    code_list = [email]
    code = singer.sign(':'.join(code_list))
    return code


def decode_email(code,max_age=15*60):
    """decode the email verify link"""
    try:
        data=get_signer().unsign(code,max_age=max_age)
    except signing.SignatureExpired:
        raise InvalidCode("The link is expired. Please request another registration link.")
    except signing.BadSignature:
        raise InvalidCode(
            'Unable to verify the signature. Please request a new'
            ' registration link.')
    email = data.rsplit(':',1)[0]
    return email


class InvalidCode(Exception):
    """Problems occurred during decoding the registration link"""
    pass


def decode_email_user(code,max_age=15*60):
    """decode the code return email user"""
    try:
        data=get_signer().unsign(code,max_age=max_age)
    except signing.SignatureExpired:
        raise InvalidCode("The link is expired. Please request another registration link.")
    except signing.BadSignature:
        raise InvalidCode(
            'Unable to verify the signature. Please request a new'
            ' registration link.')
    parts = data.rsplit(':',2)
    if len(parts) != 2:
        raise InvalidCode("Something went wrong while decoding the"
            " registration request. Please try again.")
    email,user = parts
    return email,user

def get_user_ip(request):
    """get user ip"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def save_user_ip(user,request):
    """save user login ip if the ip addr changed"""
    # if user.is_authenticated:
    user_login_ip  = get_user_ip(request)
    if user_login_ip !=user.last_login_ip:
        user.last_login_ip = user_login_ip
        user.save()