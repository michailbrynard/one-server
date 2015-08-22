from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from app_one.models import OneGroup, UserGroup, GroupImage
from app_one.serializers import OneGroupHyperSerializer, UserGroupHyperSerializer, GroupImageHyperSerializer, \
    UserHyperSerializer, ListUserGroupSerializer, SubscribeUserToGroupSerializer, ListGroupUsersSerializer, ListImageSerializer

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


# Custom Group Users view
# ---------------------------------------------------------------------------------------------------------------------#
class ListGroupUsers(generics.ListCreateAPIView):
    """
    API endpoint that list the users in a group

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token"
    http://localhost:8000/api/app_one/groups/1/

    curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT token"
    -d '{"email": "email"}'
    http://localhost:8000/api/app_one/groups/1/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    lookup_url_kwarg = "group"

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return SubscribeUserToGroupSerializer
        return ListGroupUsersSerializer

    def get_queryset(self):
        """
        This view should return a list of all the users for the group
        for the currently authenticated user.
        """
        group = self.kwargs.get(self.lookup_url_kwarg)
        return UserGroup.objects.filter(group_id=group)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        group = self.kwargs.get(self.lookup_url_kwarg)
        try:
            user_obj = UserBasic.objects.get(email=request.data['email'])
        except ObjectDoesNotExist:
            return Response({"status": "error", "message": "User does not exist."},
                            status=status.HTTP_403_FORBIDDEN)            

        if not UserGroup.objects.filter(group_id=group, user=user_obj).exists():
            data = {'user': user_obj.id,
                    'group': group
                }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"status": "success", "results":serializer.data},
                            status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"status": "error", "message": "User is already subscribed."},
                            status=status.HTTP_403_FORBIDDEN)        


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
