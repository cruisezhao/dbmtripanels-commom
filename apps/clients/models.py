from authtools.models import AbstractEmailUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from .utils import path_and_rename
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _

STATUS_CHOICES  = {
        ('Pending','Pending'),
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Canceled','Canceled'),
    }

class Clients(AbstractEmailUser):
    """user profiel use one to one field"""
    USER_TYPE={
        (1,'client'),
        (2,'reseller'),
    }
    picture = models.ImageField('Avatar',
                                upload_to=path_and_rename,
                                null=True,
                                blank=True)
    first_name = models.CharField('First name',max_length=256,null=True,blank=True)
    last_name = models.CharField('Last name',max_length=256,null=True,blank=True)
    company = models.CharField('Company',max_length=256,null=True,blank=True)
    address1 = models.CharField('Address 1',max_length=256,null=True,blank=True)
    address2 = models.CharField('Address 2',max_length=256,null=True,blank=True)
    city = models.CharField('City',max_length=256,null=True,blank=True)
    state = models.CharField('State',max_length=256,null=True,blank=True)
    postcode = models.CharField('Postcode',max_length=256,null=True,blank=True)
    country = CountryField('Country',max_length=256,null=True,blank=True)
    phone_number = PhoneNumberField('Phone Number',null=True,blank=True)
    web_site = models.URLField('Web Site',null=True,blank=True,max_length=256)
    google_plus = models.URLField('Google+',null=True,blank=True,max_length=256)
    twitter = models.URLField('Twitter',null=True,blank=True,max_length=256)
    facebook = models.URLField('Facebook',null=True,blank=True,max_length=256)
    linkedin = models.URLField('Linkedin',null=True,blank=True,max_length=256)
    alternate_email = models.EmailField('Alternate Email',null=True,blank=True,max_length=256)
    job_description = models.TextField('Job Description',null=True,blank=True)

    register_ip = models.GenericIPAddressField('Register IP',null=True,blank=True)
    register_time = models.DateTimeField('Register Time',auto_now_add = True)
    last_login_ip = models.GenericIPAddressField('Login IP',null=True,blank=True)
    last_login_time = models.DateTimeField('Login Time',auto_now = True)
    status = models.CharField('Status',max_length=32,default='Suspend',choices=STATUS_CHOICES)
    user_type = models.IntegerField('User Type',default=1,choices=USER_TYPE)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="client_set",
        related_query_name="client",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('client permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="client_set",
        related_query_name="client",
    )
    class Meta:
        db_table = 'clients'

    def format_url(self,url):
        """format the web url"""
        scheme = "https://"
        return url if scheme in url else scheme+url

    def get_web_site_url(self):
        """format user web site url"""
        return self.format_url(self.web_site)

    def get_linkedin_url(self):
        """format user web site url"""
        return self.format_url(self.linkedin)

    def get_google_plus_url(self):
        """format user google_plus url"""
        return self.format_url(self.google_plus)

    def get_twitter_url(self):
        """format user google_plus url"""
        return self.format_url(self.twitter)

    def get_facebook_url(self):
        """format user google_plus url"""
        return self.format_url(self.facebook)


class EmailTemplate(models.Model):
    """email template for send email"""
    key_word = models.CharField("Key Word",max_length=256,null=True,blank=True)
    subject = models.CharField("Subject",max_length=256,null=True,blank=True)
    body = models.TextField("Body",null=True,blank=True)

    class Meta:
        verbose_name = "email_template"
        verbose_name_plural = "email_template"

    def __str__(self):
        return "%s"  %self.key_word