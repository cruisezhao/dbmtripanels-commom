from __future__ import unicode_literals

import logging
import random
import time

from braces import views as bracesviews

from authtools import views as authviews
from .forms import  AvatarForm,\
    PasswordChangeForm, ProfileBasicForm, ProfileContactForm, ProfileSocialForm
from common.settings import base as custom_settings
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.http import cookie_date
from django.views import generic
from django.views.generic import TemplateView, RedirectView
from rest_framework_jwt.utils import jwt_encode_handler, jwt_decode_handler, jwt_payload_handler

from . import forms
from .send_mail.send_mail import send_signup_mail
from .utils import (decode_email_user, InvalidCode, get_confirmation_url,
                    save_user_ip)
import hmac
import os
from authtools.views import LoginRequiredMixin
from django.views.generic.base import View
from django.urls import reverse
from django.utils.translation import ugettext as _


Clients = get_user_model()
logger = logging.getLogger("project")



def home(request):
    """home page for test"""
    from django.http import HttpResponse
    domain = request.scheme+"://"+request.get_host()
    user = request.user
    return HttpResponse("Hello your are login in this is a succuss redirect test page,"
                        "usually it is home page.So according to different website the home page it diff. "
                        "So you will orverwrite it!".format())

class LoginView(bracesviews.AnonymousRequiredMixin,
                authviews.LoginView):
    template_name = "accounts/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        redirect = super(LoginView, self).form_valid(form)
        #save user login ip
        user = form.get_user()
        save_user_ip(user,self.request)
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me is True:
            ONE_MONTH = 30*24*60*60
            expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
            self.request.session.set_expiry(expiry)
        #set cookie token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        #redirect.set_cookie('token',token)
        max_age = custom_settings.JWT_AUTH['JWT_EXPIRATION_DELTA'].total_seconds()
        expires_time = time.time() + max_age
        expires = cookie_date(expires_time)
        redirect.set_cookie(
                            custom_settings.TOKEN_COOKIE_NAME,
                            token, 
                            max_age=max_age,
                            expires=expires, 
                            domain=custom_settings.TOKEN_COOKIE_DOMAIN or None,
                            path=custom_settings.TOKEN_COOKIE_PATH,
                            secure=custom_settings.TOKEN_COOKIE_SECURE or None,
                            httponly=custom_settings.TOKEN_COOKIE_HTTPONLY or None,
                        )
        return redirect

class LogoutView(authviews.LogoutView):
    url = reverse_lazy('home')
    
    def get(self, *args, **kwargs):
        response = super(LogoutView, self).get(*args, **kwargs)
        #delete token cookie
        #return response        
        response.delete_cookie(custom_settings.TOKEN_COOKIE_NAME, domain=custom_settings.TOKEN_COOKIE_DOMAIN)
        return response

class SignUpView(bracesviews.AnonymousRequiredMixin,
                 bracesviews.FormValidMessageMixin,
                 generic.CreateView):
    form_class = forms.SignupForm
    model = Clients
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')
    form_valid_message = """Thanks! Next, click the confirmation link that was just emailed to you.
                         If you don't see our email within a few minutes, please check your Spam
                         folder."""

    def form_valid(self, form):
        host_name = self.request.META.get('HTTP_HOST',None)
        r = super(SignUpView, self).form_valid(form)
        email = form.cleaned_data["email"]
        name = form.cleaned_data["name"]
        absolute_url = get_confirmation_url(email,self.request,name)
        try:
            query_name = Clients.objects.get(name=name)
            query_name.is_active = False
            query_name.save()
            logger.info('a new inactive user {} created'.format(query_name))
        except:
            pass
        #send email
        to = email
        send_signup_mail(name,absolute_url,to)
        return r


def confirmation_view(request, code):
    """email confirm"""
    try:
        email,username = decode_email_user(code)
    except InvalidCode as e:
        messages.warning(request,"{}".format(e))
        return HttpResponseRedirect(reverse_lazy('home'))
    try:
        user = Clients.objects.get(name = username)
    except ObjectDoesNotExist as e:
        messages.warning(request,"{}".format(e))
        return HttpResponseRedirect(reverse_lazy('home'))
    if user.is_active:
        messages.warning(request,"Your accouts has already actived!,you can login now" )
        return HttpResponseRedirect(reverse_lazy('home'))
    user.is_active = True
    user.save()
    messages.success(request,"Your accouts is active,you can login now" )
    return HttpResponseRedirect(reverse_lazy('home'))


class PasswordChangeView(authviews.PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = 'accounts/password-change.html'
    success_url = reverse_lazy('accounts:passwordchange')

    def form_valid(self, form):
        #form.save()
        logout(self.request)
        
        messages.success(self.request,
                         "Your password has changed, "
                         "hence you have been logged out. Please relogin")
        response = super(PasswordChangeView, self).form_valid(form)
        #response.delete_cookie(custom_settings.TOKEN_COOKIE_NAME, domain=custom_settings.TOKEN_COOKIE_DOMAIN)
        return response
    
    def get_context_data(self, **kwargs):
        if 'passwordchange_active' not in kwargs:
            #for nav tab display
            kwargs['passwordchange_active'] = "active"
        return super(PasswordChangeView, self).get_context_data(**kwargs)

class PasswordResetView(authviews.PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = 'accounts/password-reset.html'
    success_url = reverse_lazy('accounts:password-reset-done')
    subject_template_name = 'accounts/emails/password-reset-subject.txt'
    email_template_name = 'accounts/emails/password-reset-email.html'


class PasswordResetDoneView(authviews.PasswordResetDoneView):
    template_name = 'accounts/password-reset-done.html'


class PasswordResetConfirmView(authviews.PasswordResetConfirmAndLoginView):
    template_name = 'accounts/password-reset-confirm.html'
    form_class = forms.SetPasswordForm


        
# @login_required
# def account_page_view(request, template_name):
#     ''' list account pagae '''
#     profile_form = None
#     avatar_form = None
#     passchg_form = None
#     if request.method == 'POST':
#         if '_profile' in request.POST:
#             profile_form = ProfileForm(request.POST, instance=request.user, files=request.FILES)
#             if profile_form.is_valid():
#                 # process the data in form.cleaned_data as required
#                 profile_form.save()
#                 # redirect to a new URL:
#                 return HttpResponseRedirect(reverse('accounts:all'))
# 
#         elif '_avatar' in request.POST:
#             avatar_form = AvatarForm(request.POST, instance=request.user, files=request.FILES)
#             if avatar_form.is_valid():
#                 # process the data in form.cleaned_data as required
#                 avatar_form.save()
#                 # redirect to a new URL:
#                 return HttpResponseRedirect(reverse('accounts:all'))
#         
#         elif '_passwordchange' in request.POST:
#             passchg_form = PasswordChangeForm(request.user, data=request.POST, files=request.FILES)
#             if passchg_form.is_valid():
#                 # process the data in form.cleaned_data as required
#                 passchg_form.save()
#                 # redirect to a new URL:
#                 return HttpResponseRedirect(reverse('accounts:all'))
#    
#     if profile_form is None:        
#         profile_form = ProfileForm(instance=request.user)
#     if avatar_form is None:
#         avatar_form = AvatarForm(instance=request.user)
#     if passchg_form is None:
#         passchg_form = PasswordChangeForm(request.user)
#         
#     return render(request, template_name, {'profile_form':profile_form, 'avatar_form':avatar_form, 'passchg_form':passchg_form})

@login_required
def profile_basic(request, template_name, form_name='form'):
    ''' list and edit user profile '''
    if request.method == 'POST':
        form = ProfileBasicForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            messages.success(request, _("save successfully"))
            # redirect to a new URL:
            #return HttpResponseRedirect(reverse('accounts:profile_basic'))
    # if a GET (or any other method) we'll create a new form by user model from DB           
    else:
        user = request.user
        form = ProfileBasicForm(instance=user)
        
    return render(request, template_name, {form_name:form, 'profile_basic_active':'active'})

@login_required
def profile_contact(request, template_name, form_name='form'):
    ''' list and edit user profile '''
    if request.method == 'POST':
        if len(request.POST.get('phone_number', '').strip().split()) <= 1:
            request.POST['phone_number'] = ''
        form = ProfileContactForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            messages.success(request, _("save successfully"))
            #return HttpResponseRedirect(reverse('accounts:profile_contact'))
    # if a GET (or any other method) we'll create a new form by user model from DB           
    else:
        user = request.user
        form = ProfileContactForm(instance=user)
        
    return render(request, template_name, {form_name:form, 'profile_contact_active':'active'})

@login_required
def profile_social(request, template_name, form_name='form'):
    ''' list and edit user profile '''
    if request.method == 'POST':
        form = ProfileSocialForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            messages.success(request, _("save successfully"))
            # redirect to a new URL:
            #return HttpResponseRedirect(reverse('accounts:profile_social'))
    # if a GET (or any other method) we'll create a new form by user model from DB           
    else:
        user = request.user
        form = ProfileSocialForm(instance=user)
        
    return render(request, template_name, {form_name:form, 'profile_social_active':'active'})

@login_required
def avatar(request, template_name, form_name='avatar_form'):
    ''' update user avatar '''
    if request.method == 'POST':
        form = AvatarForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            #change photo name to name with md5(secret+email)+ current time
            oldpic = Clients.objects.get(pk=request.user.pk).picture
            
            form.save()
            #delete old photo file
            #os.remove(os.path.join(settings.MEDIA_ROOT, oldpic_path))
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('accounts:all'))
    # if a GET (or any other method) we'll create a new form by user model from DB           
#     else:
#         user = request.user
#         form = AvatarForm(instance=user)
        
        return render(request, template_name, {form_name:form})