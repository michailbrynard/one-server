import base64
from logging import getLogger
from datetime import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from app_one.models import Image, SnortieLimiter, UserFollow
from app_one.serializers import SnortieLimiterSerializer, ListImageSerializer, CreateImageSerializer
# from app_one.serializers import CreateImageSerializer, \
#     SnortieLimiterSerializer, CreateSnortieSerializer, ListFriendsSerializer, \
#     CreateFriendSerializer, ListImageSerializer

from administration.models import UserBasic

LOCAL = False
logger = getLogger('django')


# Check one status
# ---------------------------------------------------------------------------------------------------------------------#
class CheckOne(generics.ListAPIView):
    """
    API endpoint that list the user's questions, and allows an user to create a question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/1/
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = SnortieLimiterSerializer

    def get(self, request, *args, **kwargs):
        # Check if user has posted photo for the day.
        try:
            last_image = Image.objects.filter(user=self.request.user).latest('created_timestamp')
            if datetime.today().day == last_image.created_timestamp.day:
                snortie = SnortieLimiter.objects.all().order_by('?').first()
                data = {"status": "error", "message": snortie.message}
            else:
                data = {"status": "success", "message": "You are still okay."}
        except ObjectDoesNotExist:
            data = {"status": "success", "message": "You are still okay."}

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

#
# # Friends views
# # ---------------------------------------------------------------------------------------------------------------------#
# class ListCreateFriends(generics.ListCreateAPIView):
#     """
#     API endpoint that list the user's groups.
#     curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/groups/
#     """
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#
#     def get_serializer_class(self, *args, **kwargs):
#         if self.request.method == 'POST':
#             return CreateFriendSerializer
#         return ListFriendsSerializer
#
#     def get_queryset(self):
#         """
#         This view should return a list of all groups for a user
#         """
#         return UserFriend.objects.filter(user=self.request.user, friend_status='Friends')
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#
#         print(request.data['instructions'])
#
#         if request.data['instructions'] == 'invite':
#             message = "You have successfully invited a new friend."
#         elif request.data['instructions'] == 'reject':
#             message = "You have successfully rejected a friend request."
#         elif request.data['instructions'] == 'accept':
#             message = "You have successfully accepted a friend request."
#
#         return Response({"status": "success", "message": message})
#
#
# Images views
# ---------------------------------------------------------------------------------------------------------------------#
class ListImages(generics.ListAPIView):
    """
    API endpoint that lists the user's images

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ListImageSerializer
    paginate_by = 10

    def get_queryset(self):
        """
        This view should return a list of all the images related to a user.
        """
        user_obj = self.request.user
        return Image.objects.filter(user=user_obj).order_by('-id')


class ListUserImages(generics.ListAPIView):
    """
    API endpoint that lists the user's images

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ListImageSerializer
    paginate_by = 10
    lookup_url_kwarg = "user"

    def get(self, request, *args, **kwargs):
        """
        This view should return a list of all the images related to a user.
        """

        user_id = self.kwargs.get(self.lookup_url_kwarg)

        data = Image.objects.filter(user_id=user_id).order_by('-id')

        if data:
            serializer = self.get_serializer(instance=data, data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
        else:
            data = {'status': 'error', 'message': 'Sorry, this person does not exist.'}
            return Response(data)


class CreateImage(generics.ListCreateAPIView):
    """
    API endpoint that allows images to be viewed or edited.
    """
    queryset = Image.objects.all()
    serializer_class = CreateImageSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info(request.data)

        data = request.data.copy()

        logger.info('received copy of data!!')

        if isinstance(data.get('image'), str):
            logger.info('Base64 from ios:')
            imgstring = data.pop('image')[0]
            logger.info(imgstring)
            img = ContentFile(base64.b64decode(imgstring), name='image.jpg')
            # img = InMemoryUploadedFile(img, None, 'image.jpg', 'image/jpeg', len(img), None)
            data.update({'image': img})
        else:
            logger.info('In memory file')

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        logger.info('Data is valid!')
        logger.info(serializer)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# # Snorty views
# # ---------------------------------------------------------------------------------------------------------------------#
# class CreateSnorties(generics.CreateAPIView):
#     """
#     API endpoint that list the user's groups.
#     curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/snorties/
#     """
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#     serializer_class = CreateSnortieSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         try:
#             return Response({"status": "success", "results": serializer.data},
#                             status=status.HTTP_201_CREATED, headers=headers)
#         except ObjectDoesNotExist:
#             return Response({"status": "error", "message": "User could not be deleted. Please try again soon."})