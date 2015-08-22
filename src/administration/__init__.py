# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
logger = logging.getLogger('django')

# APP CONFIG
# ---------------------------------------------------------------------------------------------------------------------#
default_app_config = 'administration.apps.CustomConfig'


# APP PERMISSIONS
# ---------------------------------------------------------------------------------------------------------------------#
#from django.db.models.signals import post_syncdb
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth import models

# custom user related permissions
#def add_user_permissions(sender, **kwargs):
#    ct = ContentType.objects.get_for_model(model=models.User)
#    perm, created = models.Permission.objects.get_or_create(codename='can_use_', name='Can use ', content_type=ct)#

#post_syncdb.connect(add_user_permissions, sender=models)