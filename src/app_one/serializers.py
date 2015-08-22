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
class OneGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneGroup
        fields = ('id', 'user', 'group_name', 'group_icon', 'status', 'created_timestamp')


class UserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('id', 'user', 'group', 'status', 'created_timestamp')


class GroupImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupImage
        fields = ('id', 'user_group', 'image', 'created_timestamp')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBasic
        fields = ('id', 'username', 'first_name', 'last_name', 'birthday', 'gender', 'email', 'language', 'bio')


# Custom Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class ListUserGroupSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField(source='get_user')
    group = serializers.SerializerMethodField(source='get_group')
    last_upload = serializers.SerializerMethodField(source='get_last_upload')

    class Meta:
        model = UserGroup
        fields = ('user', 'group', 'created_timestamp', 'last_upload')

    def get_user(self, obj):
        user_obj = UserBasic.objects.get(id=obj.user_id)
        serialized_obj = UserSerializer(user_obj, context=self.context)
        return serialized_obj.data

    def get_group(self, obj):
        group_obj = OneGroup.objects.get(id=obj.group_id)
        serialized_obj = OneGroupSerializer(group_obj, context=self.context)
        return serialized_obj.data

    def get_last_upload(self, obj):
        try:
            latest = GroupImage.objects.filter(user_group=obj.id).latest('created_timestamp')
            return latest.created_timestamp
        except ObjectDoesNotExist:
            return None

