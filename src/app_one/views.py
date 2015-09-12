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

from app_one.models import OneGroup, UserGroup, GroupImage, OneImage, ImageMany, SnortieLimiter
from app_one.serializers import OneGroupHyperSerializer, UserGroupHyperSerializer, GroupImageHyperSerializer, \
    UserHyperSerializer, ListUserGroupSerializer, SubscribeUserToGroupSerializer, ListImageSerializer, \
    ListAllImageSerializer, CreateGroupSerializer, OneImageHyperSerializer, ImageManyHyperSerializer, \
    SnortieLimiterSerializer

from administration.models import UserBasic

LOCAL = False
logger = getLogger('django')


# Hyper Views
# ---------------------------------------------------------------------------------------------------------------------#
class OneGroupHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = OneGroup.objects.all()
    serializer_class = OneGroupHyperSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class UserGroupHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows user groups to be viewed or edited.
    """
    queryset = UserGroup.objects.filter()
    serializer_class = UserGroupHyperSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class GroupImageHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows group images to be viewed or edited.
    """
    queryset = GroupImage.objects.all()
    serializer_class = GroupImageHyperSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class UserHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserBasic.objects.all()

    serializer_class = UserHyperSerializer


class ImageManyHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows images to be viewed or edited.
    """
    queryset = ImageMany.objects.all()
    serializer_class = ImageManyHyperSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class OneImageHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows images to be viewed or edited.
    """
    queryset = OneImage.objects.all()
    serializer_class = OneImageHyperSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info(request.data)
        # logger.info(request.files)

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

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response({"status": "success", "results": serializer.data},
    #                     status=status.HTTP_201_CREATED, headers=headers)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response({"status": "success", "results": serializer.data},
    #                     status=status.HTTP_201_CREATED, headers=headers)


# Custom Views
# ---------------------------------------------------------------------------------------------------------------------#
class ListCreateGroups(generics.ListCreateAPIView):
    """
    API endpoint that list the user's groups.
    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/groups/
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ListUserGroupSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return CreateGroupSerializer
        return ListUserGroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all groups for a user
        """
        return UserGroup.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": "success", "results": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class ListCreateGroupUsers(generics.ListCreateAPIView):
    """
    API endpoint that lists the users in a group

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token"
    http://localhost:8888/api/app_one/groups/1/

    curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT token"
    -d '{"email": "email"}'
    http://localhost:8888/api/app_one/groups/1/
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_url_kwarg = "group"

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return SubscribeUserToGroupSerializer
        return ListUserGroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all the users for the group
        for the currently authenticated user.
        """
        group_id = self.kwargs.get(self.lookup_url_kwarg)
        one_group = OneGroup.objects.get(id=group_id)

        return UserGroup.objects.filter(group_id=group_id)
        # else:
        #     return None
        #     # return Response({
        #     #     "status": "error", "message": "Permission denied, only creators can view a groups user list."
        #     # }, status=status.HTTP_403_FORBIDDEN, )

    def perform_create(self, serializer, user_obj):
        serializer.save(user=user_obj)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        group = self.kwargs.get(self.lookup_url_kwarg)
        if not OneGroup.objects.filter(id=group, creator=self.request.user).exists():
            return Response(
                {"status": "error", "message": "Permission denied, only creators can add users to a group."},
                status=status.HTTP_403_FORBIDDEN)

        try:
            user_obj = UserBasic.objects.get(email=request.data['email'])
        except ObjectDoesNotExist:
            return Response({"status": "error", "message": "User does not exist."},
                            status=status.HTTP_200_OK)

        if not UserGroup.objects.filter(group_id=group, user=user_obj).exists():
            data = {'user': user_obj.id,
                    'group': group
                    }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer, user_obj)
            headers = self.get_success_headers(serializer.data)
            return Response({"status": "success", "results": serializer.data},
                            status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"status": "error", "message": "User is already subscribed."},
                            status=status.HTTP_200_OK)


class ListImages(generics.ListAPIView):
    """
    API endpoint that lists the user's images

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ListAllImageSerializer
    paginate_by = 10

    def get_queryset(self):
        """
        This view should return a list of all the images related to a user.
        """
        user_obj = self.request.user
        group_id_list = [x['id'] for x in user_obj.usergroup_set.values('id')]

        group_image_ids = set(
            GroupImage.objects.filter(user_group_id__in=group_id_list).values_list('image_id', flat=True))

        return OneImage.objects.filter(id__in=group_image_ids, user=user_obj).order_by('-id')


class ListImageGroups(generics.ListAPIView):
    """
    API endpoint that lists a group's images

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/1/
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ListImageSerializer
    paginate_by = 10
    lookup_url_kwarg = "group"

    def get_queryset(self):
        """
        This view should return a list of all the images related to groups.
        """
        group = self.kwargs.get(self.lookup_url_kwarg)
        user_group_obj = UserGroup.objects.get(user=self.request.user, group_id=group)
        return GroupImage.objects.filter(user_group=user_group_obj)

    # def get_serializer_class(self, *args, **kwargs):
    #     if self.request.method == 'POST':
    #         return CreateGroupSerializer
    #     return ListImageSerializer
    #
    #
    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)
    #
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    #
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response({"status": "success", "results": serializer.data},
    #                     status=status.HTTP_201_CREATED, headers=headers)


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
        last_image = OneImage.objects.filter(user_id=11).latest('created_timestamp')

        if datetime.today().day == last_image.created_timestamp.today().day:
            snortie = SnortieLimiter.objects.all().order_by('?').first()
            data = {"status": False, "message": snortie.message}
        else:
            data = {"status": True, "message": "You are still okay."}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
