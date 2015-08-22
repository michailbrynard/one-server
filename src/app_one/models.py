# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
import os
from django.db import models
from administration.models import UserBasic


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
from logging import getLogger
from django.db.models.signals import post_save

logger = getLogger('django')


# MODELS
# ---------------------------------------------------------------------------------------------------------------------#
def get_one_images_path(instance, filename):
    return os.path.join('one_images', str(instance.id), filename)


def get_group_icon_path(instance, filename):
    return os.path.join('group_icon', str(instance.id), filename)


class OneGroup(models.Model):
    # User id
    user = models.ForeignKey(UserBasic)
    # Name
    group_name = models.CharField(max_length=200, null=True, blank=True)
    # Group icon
    group_icon = models.FileField(upload_to=get_group_icon_path, null=True, blank=True)

    # Group status
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
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):  # Python 3: def __str__(self):
        return self.group_name


class UserGroup(models.Model):
    # User id
    user = models.ForeignKey(UserBasic)
    # Group id
    group = models.ForeignKey(OneGroup)
    # Timestamp
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    # Group status
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


class GroupImage(models.Model):
    # Group id
    user_group = models.ForeignKey(UserGroup)
    # Image field
    image = models.FileField(upload_to=get_one_images_path, null=True, blank=True)
    # Description
    description = models.CharField(max_length=200, null=True, blank=True)
    # Timestamp
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    # Group status
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