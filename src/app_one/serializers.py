from base64 import b64decode
from logging import getLogger
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app_one.exceptions import UserFriendClashException, FriendAlreadyInvitedException
from app_one.exceptions import FriendsExistsException
from app_one.models import Image, SnortieLimiter, UserFriend
from administration.models import UserBasic
from django.core.files.base import ContentFile

logger = getLogger('django')


# Basic Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBasic
        fields = ('id', 'username', 'first_name', 'last_name', 'birthday', 'gender', 'email', 'language', 'bio')


# Friends Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class CreateFriendSerializer(serializers.Serializer):
    email = serializers.CharField(default='')

    def create(self, validated_data):

        if UserBasic.objects.filter(email=validated_data['email']).exists():
            friend = UserBasic.objects.get(email=validated_data['email'])
            status = "Pending"
        else:
            friend = None
            status = "Invited"

        try:
            instance = UserFriend.objects.create(user=validated_data['user'],
                                                 invite_reference=validated_data['email'],
                                                 friend=friend,
                                                 friend_status=status)
            return instance
        except (UserFriendClashException, FriendsExistsException, FriendAlreadyInvitedException) as err:
            raise ValidationError({'status': 'error', 'message': err.detail})


class ListFriendsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source='get_user')
    friend = serializers.SerializerMethodField(source='get_friend')

    class Meta:
        model = UserFriend
        fields = ('user', 'friend', 'friend_status', 'invited_timestamp', 'accepted_timestamp', 'updated_timestamp')

    def get_user(self, obj):
        user_obj = UserBasic.objects.get(id=obj.user_id)
        serialized_obj = UserSerializer(user_obj, context=self.context)
        return serialized_obj.data

    def get_friend(self, obj):
        friend_obj = UserBasic.objects.get(id=obj.friend_id)
        serialized_obj = UserSerializer(friend_obj, context=self.context)
        return serialized_obj.data


# Image Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class CreateImageSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        logger.info(validated_data)

        # if model_field.get_internal_type() == "ImageField" or model_field.get_internal_type() == "FileField":  # Convert files from base64 back to a file.
        #     if field_elt.text is not None:
        #         image_data = b64decode(field_elt.text)
        #         setattr(instance, model_field.name, ContentFile(image_data, 'myImage.png'))

        instance = Image.objects.create(**validated_data)

        return instance

    class Meta:
        model = Image
        fields = ('image',)


class ListImageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source='get_user')
    created_timestamp = serializers.DateTimeField('%d %b %Y')

    class Meta:
        model = Image
        fields = ('image', 'description', 'created_timestamp', 'user')

    def get_user(self, obj):
        user_obj = UserBasic.objects.get(id=obj.user_id)
        serialized_obj = UserSerializer(user_obj, context=self.context)
        return serialized_obj.data


# Snorty Serializers
# ---------------------------------------------------------------------------------------------------------------------#
class SnortieLimiterSerializer(serializers.Serializer):
    message = serializers.CharField(default='You are still okay.')
    status = serializers.CharField(default=False)


class CreateSnortieSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = SnortieLimiter.objects.create(**validated_data)
        return instance

    class Meta:
        model = SnortieLimiter
        fields = ('message',)