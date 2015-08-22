from django.conf import settings
from django.contrib.auth import login, logout

from administration.models import UserBasic, GroupBasic, CustomToken
from administration.serializers import UserSerializer, GroupSerializer, CustomTokenSerializer, \
    LoginSerializer, TokenSerializer, PasswordChangeSerializer, \
    PasswordResetConfirmSerializer, PasswordResetSerializer
from administration.app_settings import UserDetailsSerializer

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated,  AllowAny
from rest_framework.response import Response
from rest_framework.request import Request as HttpRequest

from allauth.account import app_settings
from allauth.account.utils import complete_signup
from allauth.account.views import SignupView, ConfirmEmailView

from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserBasic.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = GroupBasic.objects.all()
    serializer_class = GroupSerializer


class Register(APIView, SignupView):

    """
    curl -X POST -H "Content-Type: application/json" -d
    '{"username":"test25", "password1":"test25", "password2":"test25",
    "email":"test25@zapgo.co"}' http://localhost:9090/api/register/

    Response: {{"status":"success","results":
    {"username":"test25","email":"test25@zapgo.co","first_name":"","last_name":""}}
    """

    permission_classes = (AllowAny,)
    user_serializer_class = UserDetailsSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def form_valid(self, form):
        self.user = form.save(self.request)
        if isinstance(self.request, HttpRequest):
            request = self.request
        else:
            request = self.request._request
        return complete_signup(request, self.user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.initial = {}
        self.request.POST = self.request.data.copy()
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if self.form.is_valid():
            self.form_valid(self.form)
            return self.get_response()
        else:
            return self.get_response_with_errors()

    def get_response(self):
        serializer = self.user_serializer_class(instance=self.user)
        return Response({"status": "success", "results": serializer.data}, status=status.HTTP_201_CREATED)

    def get_response_with_errors(self):
        error_ref = list(self.form.errors.items())[0][0]
        message = list(self.form.errors.items())[0][1][0]
        return Response({"status": "error", "error_ref": error_ref, "message": message},
                        status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView, ConfirmEmailView):

    """
    curl -X POST -H "Content-Type: application/json" -d '{"key":"key"}'
    http://localhost:9090/api/verify-email/

    Response: {"status":"success","message":"Email successfully verified"}
    """

    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        self.kwargs['key'] = self.request.data.get('key', '')
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'status': 'success', 'message': 'Email successfully verified'},
                        status=status.HTTP_200_OK)


class Login(GenericAPIView):

    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.

    curl -X POST -H "Content-Type: application/json" -d '{"username":"test1",
    "password":"test1"}' http://localhost:9090/api/login/

    Response: {"results":{"token":""},"status":"success"}
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = CustomToken
    response_serializer = CustomTokenSerializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, created = self.token_model.objects.update_or_create(
            user=self.user)
        # payload = jwt_payload_handler(self.user)
        # self.token = jwt_encode_handler(payload)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):

        return Response({"status": "success", "results": self.response_serializer(self.token).data},
                        status=status.HTTP_200_OK)

    def get_error_response(self):
        error_ref = list(self.serializer.errors.items())[0][0]
        message = list(self.serializer.errors.values())[0][0]
        return Response({"status": "error", "error_ref": error_ref, "message": message},
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            return self.get_error_response()
        self.login()
        return self.get_response()


class Logout(APIView):

    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.

    curl -X POST -H "Authorization: JWT token" http://localhost:9090/api/logout/

    Response: {"message":"Successfully logged out.","status":"success"}
    """
    permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        logout(request)

        return Response({"status": "success", "message": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class PasswordReset(GenericAPIView):

    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.

    curl -X POST -H "Content-Type: application/json" -d
    '{"email":"test5@zapgo.co"}' http://localhost:9090/api/password/reset/

    Response: {"message":"Password reset e-mail has been sent.","status":"success"}
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            error_ref = list(serializer.errors)[0]
            message = list(serializer.errors.items())[0][1][0]
            return Response({"status": "error", "error_ref": error_ref, 'message':message},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"status": "success", "message": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirm(GenericAPIView):

    """
    Password reset e-mail link is confirmed, therefore this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.

    curl -X POST -H "Content-Type: application/json" -d '{"uid":"NA",
    "token":"43z-d972fbdca89b1dc65087", "new_password1":"oooppp", "new_password2":"oooppp"}'
    http://localhost:9090/api/password/reset/confirm/

    Response: {"status":"success","message":"Password has been reset with the new password."}
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            error_ref = list(serializer.errors)[0]
            message = list(serializer.errors.items())[0][1][0]
            return Response({"status": "error", "error_ref": error_ref, 'message':message},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"status": "success", "message": "Password has been reset with the new password."})


class PasswordChange(GenericAPIView):

    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.

    curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT token"
    -d '{"new_password1":"qqqqqq", "new_password2":"qqqqqq"}'
    http://localhost:9090/api/password/change/

    Response: {"status":"success","message":"New password has been saved."}

    Error Response: {"status":"error","error_ref":"password_field","message":"Passwords have to match."}
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            error_ref = list(serializer.errors)[0]
            message = list(serializer.errors.items())[0][1][0]
            return Response({"status": "error", "error_ref": error_ref, 'message':message},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"status": "success", "message": "New password has been saved."})
