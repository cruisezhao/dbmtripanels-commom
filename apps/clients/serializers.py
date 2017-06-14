"""this module is used to serializer django model.The
    serializered model object is used to construct api"""
import traceback
from django.contrib.auth import get_user_model,authenticate
User = get_user_model()

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .utils import get_user_ip,get_confirmation_url,create_code
from .send_mail.send_mail import (send_signup_mail,send_reset_password_mail,
                                  send_general_email)


class UserLoginTokenSerializer(JSONWebTokenSerializer):
    """user serializer"""
    """user login serailzie"""
    def validate_email(self,data):
        if not data:
            raise serializers.ValidationError("This field may not be blank.")
        user = User.objects.filter(email=data)
        if not user:
            raise serializers.ValidationError("user with this name not exists.")
        return data

    def validate_password(self,data):
        if not data:
            raise serializers.ValidationError("This field may not be blank. ")
        return data

    def validate(self, attrs):
        """override the validate method"""
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'the username or password may not be true please try again.'
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class UserSignupSerializer(serializers.ModelSerializer):
    """user model serialize for sign up"""
    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self,validated_data):
        """overwrittern create method for user"""
        try:
            #save user ip
            request = self._context.get("request")
            ip = get_user_ip(request)
            user_email=validated_data['email']
            user = User.objects.create(email=user_email,register_ip=ip)
            user.set_password(validated_data["password"])
            user.save()
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    User.__name__,
                    User.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)
        send_general_email(user_email,request)
        return user

class UserPasswordSerializer(serializers.Serializer):
    """serializer for user change password"""
    password = serializers.CharField(required = True,max_length=128)
    new_password = serializers.CharField(required = True,max_length=128)
    confirm_password = serializers.CharField(required=True,max_length=128)

    def validate_password(self,data):
        """check password"""
        if not self.instance.check_password(data):
            raise serializers.ValidationError("the old password is wrong!")
        return data

    def validate(self,data):
        """check new password and old password"""
        if not data["new_password"] == data["confirm_password"]:
            raise serializers.ValidationError("the password you set is different! please input again!")
        if data["password"] ==data["confirm_password"]:
            raise serializers.ValidationError("the password you set must be different from the old password!")
        return data

    def update(self, instance, validated_data):
        """update for save user password"""
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance


class UserResetPasswordSerializer(serializers.Serializer):
    """user reset password input email"""
    email = serializers.EmailField(required=True)

    def validate(self,data):
        """email valide"""
        try:
            u = User.objects.get(email = data.get("email"))
        except:
            raise serializers.ValidationError("the email you are input is not register,"
                                              "please sign-up first")
        return data

    def update(self,instance,validated_data):
        """update for send verify email"""
        email = validated_data["email"]
        request = self._context['request']
        send_general_email(email,request)
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    """user input password"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self,data):
        """validate data"""
        # if data["password"] != data["confirm_password"]:
        #     raise serializers.ValidationError("the password you set is different! please input again!")
        return data

    def update(self,instance,validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
