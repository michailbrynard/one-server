from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from app_one.models import OneGroup, UserGroup, GroupImage
from administration.models import UserBasic


# Hyperlink Api
# ---------------------------------------------------------------------------------------------------------------------#
class OneGroupHyperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OneGroup
        fields = ('id', 'user', 'group_name', 'group_icon', 'status', 'created_timestamp')


class UserGroupHyperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('id', 'user', 'group', 'status', 'created_timestamp')


class GroupImageHyperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GroupImage
        fields = ('id', 'user_group', 'image', 'created_timestamp')


class UserHyperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserBasic
        fields = ('id', 'username', 'first_name', 'last_name', 'birthday', 'gender', 'email', 'language', 'bio')


# Custom Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class OneGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OneGroup
        fields = ('id', 'user', 'group_name', 'group_icon', 'status', 'created_timestamp')


class UserGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('id', 'user', 'group', 'status', 'created_timestamp')


class GroupImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GroupImage
        fields = ('id', 'user_group', 'image', 'created_timestamp')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserBasic
        fields = ('id', 'username', 'first_name', 'last_name', 'birthday', 'gender', 'email', 'language', 'bio')

