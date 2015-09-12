from base64 import b64decode
from logging import getLogger
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from app_one.models import OneImage, OneGroup, UserGroup, GroupImage, ImageMany, SnortieLimiter
from administration.models import UserBasic
from django.core.files.base import ContentFile

logger = getLogger('django')


# Hyperlink Api
# ---------------------------------------------------------------------------------------------------------------------#
class OneGroupHyperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OneGroup
        fields = ('id', 'creator', 'group_name', 'group_icon', 'status', 'created_timestamp')


class UserGroupHyperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('id', 'user', 'group', 'status', 'created_timestamp')


class GroupImageHyperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GroupImage


class ImageManyHyperSerializer(serializers.HyperlinkedModelSerializer):
    groups = OneGroupHyperSerializer(many=True)

    class Meta:
        model = ImageMany
        fields = ('image', 'user', 'groups')
        

class OneImageHyperSerializer(serializers.HyperlinkedModelSerializer):
    # group_image = GroupImageHyperSerializer()

    def create(self, validated_data):
        logger.info(validated_data)
        # if model_field.get_internal_type() == "ImageField" or model_field.get_internal_type() == "FileField":  # Convert files from base64 back to a file.
        #     if field_elt.text is not None:
        #         image_data = b64decode(field_elt.text)
        #         setattr(instance, model_field.name, ContentFile(image_data, 'myImage.png'))

        instance = OneImage.objects.create(**validated_data)

        group_list = self.context['view'].kwargs['group_list']
        group_list = group_list.split(',')

        # groups = instance.user.usergroup_set.all()
        groups = UserGroup.objects.filter(group__in=group_list, user=instance.user)
        for group in groups:
            user_group = UserGroup.objects.filter(group_id=group.group_id)
            for u in user_group:
                GroupImage.objects.create(image=instance, user_group=u)

        return instance

    class Meta:
        model = OneImage
        fields = ('image',)


class UserHyperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserBasic
        fields = ('id', 'username', 'first_name', 'last_name', 'birthday', 'gender', 'email', 'language', 'bio')


# Basic Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class OneImageDisplaySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source='get_user')
    created_timestamp = serializers.DateTimeField('%d %b %Y')

    class Meta:
        model = OneImage
        fields = ('image', 'description', 'created_timestamp', 'user')

    def get_user(self, obj):
        user_obj = UserBasic.objects.get(id=obj.user_id)
        serialized_obj = UserSerializer(user_obj, context=self.context)
        return serialized_obj.data


class OneGroupSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField(source='get_creator')
    created_timestamp = serializers.DateTimeField('%d %b %Y')

    class Meta:
        model = OneGroup
        fields = ('id', 'creator', 'group_name', 'group_icon', 'status', 'created_timestamp')

    def get_creator(self, obj):
        creator_obj = UserBasic.objects.get(id=obj.creator_id)
        serialized_obj = UserSerializer(creator_obj, context=self.context)
        return serialized_obj.data


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


class SnortieLimiterSerializer(serializers.Serializer):
    message = serializers.CharField(default='You are still okay.')
    status = serializers.CharField(default=False)


# Custom Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class ListUserGroupSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source='get_user')
    group = serializers.SerializerMethodField(source='get_group')
    last_upload = serializers.SerializerMethodField(source='get_last_upload')
    created_timestamp = serializers.DateTimeField('%d %b %Y')

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
            return latest.created_timestamp.strftime('%d %b %Y')
        except ObjectDoesNotExist:
            return None


class CreateGroupSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        instance = OneGroup.objects.create(**validated_data)
        owner = instance.creator
        UserGroup.objects.create(user=owner, group=instance)
        return instance

    class Meta:
        model = OneGroup
        fields = ('group_name',)


class SubscribeUserToGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('user', 'group', 'created_timestamp', 'updated_timestamp')


class SubUserGroupSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source='get_user')
    group = serializers.SerializerMethodField(source='get_group')

    class Meta:
        model = UserGroup
        fields = ('id', 'user', 'group', 'status', 'created_timestamp')

    def get_user(self, obj):
        user_obj = UserBasic.objects.get(id=obj.user_id)
        serialized_obj = UserSerializer(user_obj, context=self.context)
        return serialized_obj.data

    def get_group(self, obj):
        group_obj = OneGroup.objects.get(id=obj.group_id)
        serialized_obj = OneGroupSerializer(group_obj, context=self.context)
        return serialized_obj.data


class ListAllImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='get_image')

    class Meta:
        model = GroupImage
        fields = ('id', 'image')

    def get_image(self, obj):
        image_obj = OneImage.objects.get(id=obj.id)
        serialized_obj = OneImageDisplaySerializer(image_obj, context=self.context)
        return serialized_obj.data


class ListImageSerializer(serializers.ModelSerializer):
    user_group = serializers.SerializerMethodField(source='get_user_group')
    image = serializers.SerializerMethodField(source='get_image')
    created_timestamp = serializers.DateTimeField('%d %b %Y')

    class Meta:
        model = GroupImage
        fields = ('id', 'user_group', 'image', 'created_timestamp')

    def get_user_group(self, obj):
        user_group_obj = UserGroup.objects.get(id=obj.user_group_id)
        serialized_obj = SubUserGroupSerializer(user_group_obj, context=self.context)
        return serialized_obj.data

    def get_image(self, obj):
        image_obj = OneImage.objects.get(id=obj.image_id)
        serialized_obj = OneImageDisplaySerializer(image_obj, context=self.context)
        return serialized_obj.data

