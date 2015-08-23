from logging import getLogger
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from app_one.models import OneGroup, UserGroup, GroupImage, OneImage, ImageMany
from app_one.serializers import OneGroupHyperSerializer, UserGroupHyperSerializer, GroupImageHyperSerializer, \
    UserHyperSerializer, ListUserGroupSerializer, SubscribeUserToGroupSerializer, ListImageSerializer, \
    CreateGroupSerializer, OneImageHyperSerializer, ImageManyHyperSerializer

from administration.models import UserBasic

LOCAL = False

# Hyper Views
# ---------------------------------------------------------------------------------------------------------------------#
class OneGroupHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = OneGroup.objects.all()
    serializer_class = OneGroupHyperSerializer


class UserGroupHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed or edited.
    """
    queryset = UserGroup.objects.filter()
    serializer_class = UserGroupHyperSerializer


class GroupImageHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = GroupImage.objects.all()
    serializer_class = GroupImageHyperSerializer
    if not LOCAL:
        authentication_classes = (JSONWebTokenAuthentication,)

    permission_classes = (IsAuthenticated,)


class UserHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = UserBasic.objects.all()

    serializer_class = UserHyperSerializer


class ImageManyHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = ImageMany.objects.all()
    serializer_class = ImageManyHyperSerializer
    if not LOCAL:
        authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


logger = getLogger('django')

class OneImageHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = OneImage.objects.all()
    serializer_class = OneImageHyperSerializer
    if not LOCAL:
        authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info(request.data)
        # logger.info(request.files)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

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
    API endpoint that list the user's questions, and allows an user to create a question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/groups/
    """
    permission_classes = (IsAuthenticated,)
    if not LOCAL:
        authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ListUserGroupSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return CreateGroupSerializer
        return ListUserGroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all the questions
        for the currently authenticated user.
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
    API endpoint that list the users in a group

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token"
    http://localhost:8000/api/app_one/groups/1/

    curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT token"
    -d '{"email": "email"}'
    http://localhost:8000/api/app_one/groups/1/
    """
    permission_classes = (IsAuthenticated,)
    if not LOCAL:
        authentication_classes = (JSONWebTokenAuthentication,)
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

        # if one_group.creator.id != self.request.user.id:
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
    API endpoint that list the user's questions, and allows an user to create a question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/
    """
    permission_classes = (IsAuthenticated,)
    if not LOCAL:
        authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ListImageSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Images related to groups.
        """
        user_obj = self.request.user
        group_id_list = [x['id'] for x in user_obj.onegroup_set.values('id')]

        group_image_ids = set(
            GroupImage.objects.filter(user_group_id__in=group_id_list).values_list('image_id', flat=True))

        return GroupImage.objects.filter(image_id__in=group_image_ids)


class ListImageGroups(generics.ListAPIView):
    """
    API endpoint that list the user's questions, and allows an user to create a question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/1/
    """
    permission_classes = (IsAuthenticated,)
    if not LOCAL:
        authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = ListImageSerializer

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
