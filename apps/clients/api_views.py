"""this module create api, the api is used in potal project"""
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,UpdateAPIView,GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler,jwt_get_username_from_payload_handler
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

from .serializers import \
    (UserLoginTokenSerializer,UserSignupSerializer,UserPasswordSerializer,
     UserResetPasswordSerializer,ResetPasswordSerializer)
from .utils import save_user_ip,decode_email
from django.contrib.auth import login
from .send_mail.send_mail import send_general_email


class LoginConfirm(APIView):
    """login confirm"""
    permission_classes = [AllowAny,]

    @csrf_exempt
    def post(self,request,format=None):
        data = {}
        try:
            token = request.data.get("token",None)
            payload = jwt_decode_handler(token)
            name = jwt_get_username_from_payload_handler(payload)
            user = User.objects.get(email=name)
            username = "{} {}".format(user.first_name,user.last_name) if (user.first_name and user.first_name) else user.email
            response_data = {'username':username}
        except:
            error = {"error":"can not login,please login again"}
            return Response(error,status=HTTP_400_BAD_REQUEST)
        return Response(response_data,status=HTTP_200_OK)


class UserLoginTokenAPIView(JSONWebTokenAPIView):
    """user login if succuss return token
     :para:[email password]
     :return token or error messages
    """
    serializer_class = UserLoginTokenSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            #save user ip addr
            save_user_ip(user,request)
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response_data['user'] ="{} {}".format(user.first_name,user.last_name) if (user.first_name and user.first_name) else user.email

            return Response(response_data,status=HTTP_200_OK)
            #response['Access-Control-Allow-Origin'] =
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserSignUpAPI(CreateAPIView):
    """user sign up api"""
    model = User
    permission_classes = [AllowAny,]
    serializer_class = UserSignupSerializer


class UserPasswordUpdateAPI(UpdateModelMixin,GenericAPIView):
    """reset password api"""
    permission_classes = [IsAuthenticated,]
    serializer_class = UserPasswordSerializer
    # queryset = User.objects.all()

    def get_object(self, queryset=None):
        """get user object"""
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    def update(self,request, *args, **kwargs):
        """over write update"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            error = serializer.errors
            e = {"error":[]}
            for key in error:
                e["error"].extend(error[key])
            # print(e,type(e))
            # print(error,type(error))
            return Response(e, status=HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)

        return Response("Success.", status=HTTP_200_OK)


class UserInputEmailAPI(UpdateAPIView):
    """user change password api"""
    permission_classes = [AllowAny,]
    serializer_class = UserResetPasswordSerializer

    def get_object(self, queryset=None):
        """get user object"""
        user_email = self.request.data.get("email")
        try:
            obj = User.objects.get(email=user_email)
        except:
            obj = None
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PasswordResetConfirmAPI(UpdateAPIView):
    """password reset confirm"""
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny,]

    def get_object(self, queryset=None):
        """get user object"""
        email = self.request.POST.get('email',None)
        try:
            obj = User.objects.get(email=email)
        except:
            obj = None
        return obj

    def update(self,request, *args, **kwargs):
        """overide update"""
        instance = self.get_object()
        if not instance:
            return Response("You input a wrong email,please make sure"
                            " you have register.",status=HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            error = serializer.errors
            e = {"error":[]}
            for key in error:
                e["error"].extend(error[key])
            # print(e,type(e))
            # print(error,type(error))
            return Response(e, status=HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response("Success.", status=HTTP_200_OK)


class PasswordResetValidate(APIView):
    """password reset validate"""
    permission_classes = [AllowAny,]

    @csrf_exempt
    def post(self,request,format=None):
        try:
            code = request.data.get("code",None)
            username = decode_email(code)
            response_data = {'username':username}
        except:
            error = {"error":"the link is expires,please verify a new link."}
            return Response(error,status=HTTP_400_BAD_REQUEST)
        return Response(response_data,status=HTTP_200_OK)


class SendEmailAPI(APIView):
    """send email api"""
    permission_classes = [AllowAny,]

    @csrf_exempt
    def post(self,request,format=None):
        try:
            email = request.data.get("email",None)
            send_general_email(email,request)
            response_data = {'data':'send email success'}
        except:
            error = {"error":"some error occured please contact support team."}
            return Response(error,status=HTTP_400_BAD_REQUEST)
        return Response(response_data,status=HTTP_200_OK)
