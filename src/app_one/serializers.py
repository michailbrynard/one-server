from base64 import b64decode
from logging import getLogger
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app_one.exceptions import UserFriendClashException, FriendAlreadyInvitedException, \
    RemoveUserFriendNotExistException, InviteErrorException, InviteRepeatException, DontTryLuckException, \
    FriendRejectedException
from app_one.exceptions import FriendsExistsException
from app_one.models import Image, SnortieLimiter, UserFollow
from administration.models import UserBasic
from django.core.files.base import ContentFile

logger = getLogger('django')


# # Basic Serializers
# # ---------------------------------------------------------------------------------------------------------------------#
# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = UserBasic
#         fields = ('id', 'username', 'first_name', 'last_name', 'birthday', 'gender', 'email', 'language', 'bio')
#
#
# # Friends Serializers
# # ---------------------------------------------------------------------------------------------------------------------#
# class CreateFriendSerializer(serializers.Serializer):
#     email = serializers.CharField(required=True)
#     instructions = serializers.CharField(required=True)
#
#     def create(self, validated_data):
#
#         if validated_data['instructions'] == 'invite':
#             status = 'Pending'
#         elif validated_data['instructions'] == 'reject':
#             status = 'Rejected'
#         elif validated_data['instructions'] == 'accept':
#             status = 'Friends'
#
#         try:
#
#             if UserBasic.objects.filter(email=validated_data['email']).exists():
#                 friend = UserBasic.objects.get(email=validated_data['email'])
#             else:
#                 if validated_data['instructions'] == 'invite':
#                     friend = None
#                     status = "Invited"
#
#             if UserFriend.objects.filter(user=validated_data['user'], invite_reference=validated_data['email']).exists():
#                 instance = UserFriend.objects.get(user=validated_data['user'], invite_reference=validated_data['email'])
#
#                 if status == instance.friend_status:
#                     raise InviteRepeatException()
#                 elif instance.friend_status == 'Friends':
#                     raise FriendsExistsException()
#                 elif instance.friend_status == 'Rejected':
#                     raise FriendRejectedException()
#                 elif status == 'Rejected' or status == 'Invite' or status == 'Pending':
#                     instance.friend_status = status
#                     instance.save()
#                 else:
#                     raise InviteErrorException()
#
#             else:
#                 if status == 'Pending' or status == 'Invited':
#                     instance = UserFriend.objects.create(user=validated_data['user'],
#                                                          invite_reference=validated_data['email'],
#                                                          friend=friend,
#                                                          friend_status=status)
#                 else:
#                     raise DontTryLuckException()
#
#             return instance
#
#         except (UserFriendClashException, FriendsExistsException, FriendAlreadyInvitedException,
#                 InviteErrorException, RemoveUserFriendNotExistException, InviteRepeatException,
#                 DontTryLuckException) as err:
#             raise ValidationError({'status': 'error', 'message': err.detail})
#
#
# class ListFriendsSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField(source='get_user')
#     friend = serializers.SerializerMethodField(source='get_friend')
#
#     class Meta:
#         model = UserFriend
#         fields = ('user', 'friend', 'friend_status', 'invited_timestamp', 'accepted_timestamp', 'updated_timestamp')
#
#     def get_user(self, obj):
#         user_obj = UserBasic.objects.get(id=obj.user_id)
#         serialized_obj = UserSerializer(user_obj, context=self.context)
#         return serialized_obj.data
#
#     def get_friend(self, obj):
#         friend_obj = UserBasic.objects.get(id=obj.friend_id)
#         serialized_obj = UserSerializer(friend_obj, context=self.context)
#         return serialized_obj.data
#
#
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
    # user = serializers.SerializerMethodField(source='get_user')
    created_timestamp = serializers.DateTimeField('%d %b %Y')

    class Meta:
        model = Image
        fields = ('image', 'description', 'created_timestamp')

    # def get_user(self, obj):
    #     user_obj = UserBasic.objects.get(id=obj.user_id)
    #     serialized_obj = UserSerializer(user_obj, context=self.context)
    #     return serialized_obj.data
#
#
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