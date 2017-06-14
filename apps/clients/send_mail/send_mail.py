from django.core.mail import EmailMultiAlternatives
from ..utils import create_code
from ..models import EmailTemplate
from django.conf import settings

def send_signup_mail(name,url,to):
    """user sign up mail send"""
    html_content = """<h3>Hi: %s </h3><p>Please confirm your account by clicking on the following link:
        <a href='%s'>Confirm My Account</a><br><p><b>,the confirm email will expired in 15 minutes.
        If you did not sign up for this account, you can disregard this email and the account will not be created.
        </b></p><br>
        Regards,<br>
        The DataBaseMart Team""" %(name,url)
    print(html_content)
    msg = EmailMultiAlternatives('DBM account registration confirmation', html_content, 'Taylor@jucuyun.com', [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_reset_password_mail(name,url,to):
    """user reset mail send"""
    html_content = """<h3>Hi: %s </h3><p>Please reset your password by clicking on the following link:
        <a href='%s'>Reset My Password</a><br><p><b>.
        If you did not sign up for this account, you can disregard this email.
        </b></p><br>
        Regards,<br>
        The DataBaseMart Team""" %(name,url)
    # print(html_content)
    msg = EmailMultiAlternatives('DBM account password reset', html_content, 'Taylor@jucuyun.com', [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_msg(email,addr,request,code):
    """msg send to the user"""
    from django.core.urlresolvers import resolve
    path = request.get_full_path()
    key_word = resolve(path).url_name
    try:
        e_template = EmailTemplate.objects.get(key_word=key_word)
        html_content = e_template.body.format(name=email,domain=addr,code=code)
        subject = e_template.subject
        msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [email,])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    except:
        pass
        print("send email failed.")


def send_general_email(email,request):
    """general email can use for general purpose that need some token to
    callback"""
    code = create_code(email)
    domain = request.scheme+"://"+request.get_host()
    send_msg(email,domain,request,code)
