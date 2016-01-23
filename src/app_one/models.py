# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
import os
from django.db import models
from administration.models import UserBasic


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
from logging import getLogger
from django.db.models.signals import post_save
from app_one.exceptions import FriendsExistsException, UserFriendClashException, FriendAlreadyInvitedException

logger = getLogger('django')


# MODELS
# ---------------------------------------------------------------------------------------------------------------------#
def get_one_images_path(instance, filename):
    return os.path.join('one_images', filename)


def get_group_icon_path(instance, filename):
    return os.path.join('group_icon', filename)


class Image(models.Model):
    user = models.ForeignKey(UserBasic)
    image = models.ImageField(upload_to=get_one_images_path, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class UserFriend(models.Model):
    user = models.ForeignKey(UserBasic, related_name='user')
    invite_reference = models.CharField(max_length=200, null=True, blank=True)
    friend = models.ForeignKey(UserBasic, related_name='friend', null=True, blank=True)

    # Friend status
    STATUS = (
        ('Invited', 'Invited'),
        ('Pending', 'Pending'),
        ('Friends', 'Friends'),
        ('Declined', 'Declined'),
        ('Removed', 'Removed'),
        ('NotOnOneYet', 'NotOnOneYet')
    )

    friend_status = models.CharField(
        max_length=15,
        choices=STATUS,
        default='Invited',
        null=False,
        blank=False,
    )

    invited_timestamp = models.DateTimeField(auto_now_add=True)
    accepted_timestamp = models.DateTimeField(null=True, blank=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):  # Python 3: def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):

        if UserBasic.objects.filter(email=self.invite_reference).exists():
            friend = UserBasic.objects.get(email=self.invite_reference)
            if UserFriend.objects.filter(user=self.user, friend=friend).exists():
                raise FriendsExistsException()
            elif self.user == friend:
                raise UserFriendClashException()
        elif UserFriend.objects.filter(invite_reference=self.invite_reference).exists():
            raise FriendAlreadyInvitedException()

        super(UserFriend, self).save(*args, **kwargs)


class SnortieReminder(models.Model):
    # User id
    creator = models.ForeignKey(UserBasic)
    # Reminder message when user forgets to post a picture.
    message = models.TextField(null=True, blank=True)

    ACTIVE = 'A'
    DISABLED = 'D'

    # Status
    STATUS = (
        (ACTIVE, 'Active'),
        (DISABLED, 'Disabled'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE,
        null=False,
        blank=False,
    )
    # Timestamp
    created_timestamp = models.DateTimeField(auto_now_add=True)


class SnortieLimiter(models.Model):
    # User id
    creator = models.ForeignKey(UserBasic)
    # Limiting message when user tries to post more than one picture per day.
    message = models.TextField(null=True, blank=True)
    # Status
    ACTIVE = 'A'
    DISABLED = 'D'

    STATUS = (
        (ACTIVE, 'Active'),
        (DISABLED, 'Disabled'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE,
        null=False,
        blank=False,
    )
    # Timestamp
    created_timestamp = models.DateTimeField(auto_now_add=True)