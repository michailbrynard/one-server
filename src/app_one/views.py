from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from app_one.models import OneGroup, UserGroup, GroupImage
from app_one.serializers import OneGroupHyperSerializer, UserGroupHyperSerializer, GroupImageHyperSerializer, \
    UserHyperSerializer, ListUserGroupSerializer, ListImageSerializer

from administration.models import UserBasic

import json


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


class UserHyper(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = UserBasic.objects.all()
    serializer_class = UserHyperSerializer


# Custom Views
# ---------------------------------------------------------------------------------------------------------------------#
class ListUserGroup(generics.ListAPIView):
    """
    API endpoint that list the user's questions, and allows an user to create a question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/groups/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = ListUserGroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all the questions
        for the currently authenticated user.
        """
        return UserGroup.objects.filter(user=self.request.user)


class ListImages(generics.ListAPIView):
    """
    API endpoint that list the user's questions, and allows an user to create a question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = ListImageSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Images related to groups.
        """
        user_obj = self.request.user
        group_id_list = [x['id'] for x in user_obj.onegroup_set.values('id')]
        return GroupImage.objects.filter(user_group_id__in=group_id_list)


class ListImagesGroup(generics.ListAPIView):
    """
    API endpoint that list the user's questions, and allows an user to create a question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:8888/api/images/1/
    """
    permission_classes = (IsAuthenticated, )
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