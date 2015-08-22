# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
from django.contrib import admin
from rest_framework import routers
from app_one import views

admin.autodiscover()


logger = logging.getLogger('django')


# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
# conf.urls
from django.conf.urls import patterns, url, include

# ROUTERS
# ---------------------------------------------------------------------------------------------------------------------#
router = routers.DefaultRouter()
router.register(r'hyper/groups', views.OneGroupHyper)
router.register(r'hyper/user_groups', views.UserGroupHyper)
router.register(r'hyper/group_images', views.GroupImageHyper)

# URLS
# ---------------------------------------------------------------------------------------------------------------------#
urlpatterns = patterns('',

    # Router fields - API
    url(r'^', include(router.urls)),

)