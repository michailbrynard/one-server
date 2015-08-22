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


# Basic Serializers
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


# Custom Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class ListUserGroupSerializer(serializers.ModelSerializer):

    last_upload = serializers.SerializerMethodField(source='get_last_upload')

    class Meta:
        model = UserGroup
        fields = ('user', 'group_name', 'group_icon', 'created_timestamp', 'last_upload')

    def get_last_upload(self, obj):
        try:
            latest = GroupImage.objects.latest(group=obj.id)
            return latest.created_timestamp
        except ObjectDoesNotExist:
            return None


class CreateUserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('user', 'group_name', 'group_icon', 'created_timestamp')

